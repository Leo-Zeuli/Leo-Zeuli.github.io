var features = [["The Rehearsal","a"],["The Batman","a"],["The Righteous Gemstones","r"],["Succession","a"],["Fight Club","a"],["I want to feel fear","p"],["Watchmen","a"],["Scooby Doo!","a"],["Feelings","c"],["Drunk Skeletons","ar"],["Humanoid","ar"],["Space Nightmare","ar"],["Sensation","ar"],["Revolution Storyboard","s"],["Books and Movies","a"],["Black Widow","a"],["Bored to Death","r"],["Bored to Death S1","r"],["Texas Chainsaw Massacre","a"],["Blade Runner 2049","a"],["Loki","r"]];
var features_loaded = new Array(features.length).fill(false);
 
var pointer = 0;
const parent_folder_dictionary = {"a":"Features","r":"Features","s":"Narratives","p":"Narratives","ar":"Art","c":"Art"}

function push_pointer(type=[]) {
  function check() {
    if (pointer >= features.length) {
      $(".load-more").attr("hidden",true);
      return true;
    }
  }
  if (check()) {
    return;
  }
  while (!type.includes(features[pointer][1]) && (type.length != 0)) {
    pointer += 1;
    console.log(features[pointer]);
    if (check()) {
      return;
    }
  }
}

function load_synopses(number_of_synopses, type=[]) {
  var end_index = pointer+number_of_synopses;
  pointer += number_of_synopses;
  for (let i = end_index-number_of_synopses; i < Math.min(end_index,features.length); i++) {
    if (type.includes(features[i][1]) || (type.length == 0)) {
      $.get(parent_folder_dictionary[features[i][1]]+"/"+features[i][0]+"/Synopsis.html", function(data) {
        var div = document.createElement("div");
        div.setAttribute("id", i);
        div.innerHTML = data;
        let place_before = features_loaded.indexOf(true,i+1);
        if (place_before == -1) {
          document.getElementById("synopses").appendChild(div);
        } else {
          $("#"+place_before).before(div);
        }
        features_loaded[i] = true;
      }).fail(function() {
        load_synopses(1, type);
      });
    } else {
      end_index += 1;
      pointer += 1;
    }
  }
  push_pointer(type);
}

function load_synopsis_wide(type=[]) {
  if (!document.getElementById("wide-synopses").hasChildNodes()) {
    while (!(type.includes(features[pointer][1])) && !(type.length == 0)) {
      pointer += 1;
    }
    var div = document.createElement('div');
    div.setAttribute("style", "margin: 25px 0 15px 0");
    div.setAttribute("id", "wide");
    document.getElementById("wide-synopses").appendChild(div);
    $("#wide").load(parent_folder_dictionary[features[pointer][1]]+"/"+features[pointer][0].replaceAll(" ","%20")+"/Synopsis%20Wide.html");
    pointer += 1;
  }
  push_pointer(type);
}

function load_synopses_compact(number_of_synopses, type=[]) {
  var end_index = pointer+number_of_synopses;
  pointer += number_of_synopses;
  for (let i = end_index-number_of_synopses; i < Math.min(end_index,features.length); i++) {
    if (type.includes(features[i][1]) || (type.length == 0)) {
      $.get(parent_folder_dictionary[features[i][1]]+"/"+features[i][0]+"/Synopsis%20Compact.html", function(data) {
        var div = document.createElement("div");
        div.setAttribute("class", "compact-alignment");
        div.setAttribute("id", i);
        div.innerHTML = data;
        let place_before = features_loaded.indexOf(true,i+1);
        if (place_before == -1) {
          document.getElementById("compact-synopses").appendChild(div);
        } else {
          $("#"+place_before).before(div);
        }
        features_loaded[i] = true;
      }).fail(function() {
        load_synopses_compact(1);
      });
    } else {
      end_index += 1;
      pointer += 1;
    }
  }
  push_pointer(type);
}

function load_art(per_row,number_of_rows, pieces=[]) {
  var piece_synopses = Array(number_of_rows).fill(undefined).map(e => Array(per_row).fill(undefined));
  var pieces_to_load = per_row*number_of_rows;
  var in_progress = 0;
  var isRunning;

  function load_pieces(pieces_to_load) {
    var compact_container = document.createElement("div");
    compact_container.setAttribute("class", "art-flexbox-container");
    var ratio_sum = 0;
    for (img of pieces_to_load) {
      ratio_sum += img[1]/img[2];
    }
    var height = parseInt((800-5*(pieces_to_load.length-1))/ratio_sum);
    for (piece of pieces_to_load) {
      piece[0].firstElementChild.firstElementChild.setAttribute("style","max-height:"+String(height)+"px");
      compact_container.appendChild(piece[0]);
    }
    document.getElementById("collection-synopses").appendChild(compact_container);
  }

  function find_undefined() {
    for (var i = 0; i < piece_synopses.length; i++){
      for (var j = 0; j < piece_synopses[i].length; j++) {
        if (piece_synopses[i][j] == undefined){
          return([i,j]);
        }
      }
    }
  }

  function load_remaining() {
    if (pointer >= features.length) {
      pieces_to_load = 0;
      for (row of piece_synopses) {
        filtered_row = row.filter(function(element){return (element != undefined)});
        if (filtered_row.length != 0) {
          load_pieces(filtered_row);
        }
      }
    }
    push_pointer(["ar"]);
  }

  function load_piece(source) {
    pieces_to_load -= 1;
    $.get("/Art/"+source+"/Linked%20Piece.html", function(data) {
      in_progress += 1;
      var div = document.createElement("div");
      div.innerHTML = data;
      var img = new Image();
      img.onload = function() {
        index = find_undefined();
        piece_synopses[index[0]][index[1]] = [div,this.naturalWidth,this.naturalHeight];
        for (var row = 0; row < piece_synopses.length; row++) {
          if (!piece_synopses[row].includes(undefined)) {
            load_pieces(piece_synopses[row]);
            piece_synopses[row] = [];
          }
        }
        in_progress -= 1;
        if ((in_progress <= 0) && (!isRunning)){
          load_remaining();
        }
      };
      img.src = div.firstElementChild.firstElementChild.getAttribute('src');
    }).fail(function() {
      in_progress -= 1;
      pieces_to_load += 1; 
      if (!isRunning && (pieces.length != 0)) {fill_piece_synopses()};
    });
  }

  if (pieces.length != 0) {
    isRunning = true;
    pointer = features.length;
    for (piece of pieces) {
      if (pieces_to_load != 0){
        load_piece(piece);
      }
    }
    isRunning = false;
    load_remaining();
  }

  else {
    function fill_piece_synopses() {
      isRunning = true;

      if (pointer >= features.length) {
        load_remaining();
      }

      while (pieces_to_load != 0) {
        if (features[pointer][1] == "ar"){
          load_piece(features[pointer][0]);
        }
        pointer += 1;
        if (pointer >= features.length) {
          load_remaining();
        }
      };
      isRunning = false;
    }
    fill_piece_synopses()
  }
  push_pointer(["ar"]);
}

function load_more(source) {
  if (source == "index") {
    load_synopsis_wide(["r","a","s","p","c"]);
    load_synopses_compact(9,["r","a","s","p","c"]);
  } else if (source == "reviews") {
    load_synopses(6,["r"]);
  } else if (source == "analyses") {
    load_synopses(6,["a"]);
  } else if (source == "features") {
    load_synopses(6,["r","a"]);
  } else if (source == "screenplays") {
    load_synopses(6,["s"]);
  } else if (source == "prose") {
    load_synopses(6,["p"]);
  } else if (source == "narratives") {
    load_synopses(6,["s","p"]);
  } else if (source == "art") {
    load_art(3,3);
  }
};
