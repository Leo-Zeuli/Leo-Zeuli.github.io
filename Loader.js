var features = [["Revolution Storyboard","s"],["Books and Movies","a"],["Black Widow","a"],["Bored to Death","r"],["Bored to Death S1","r"],["Texas Chainsaw Massacre","a"],["Blade Runner 2049","a"],["Loki","r"]];
var features_loaded = new Array(features.length).fill(false);

var synopsis_pointer = 0;
const parent_folder_dictionary = {"a":"Features","r":"Features","s":"Narratives","p":"Narratives","ar":"Art","c":"Art"}

function push_pointer(type=[]) {
  function check() {
    if (synopsis_pointer >= features.length) {
      $(".load-more").attr("hidden",true);
      return true;
    }
  }
  if (check()) {
    return;
  }
  while (!type.includes(features[synopsis_pointer][1]) && (type.length != 0)) {
    synopsis_pointer += 1;
    console.log(features[synopsis_pointer]);
    if (check()) {
      return;
    }
  }
}
function load_synopses(number_of_synopses, type=[]) {
  var end_index = synopsis_pointer+number_of_synopses;
  synopsis_pointer += number_of_synopses;
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
      synopsis_pointer += 1;
    }
  }
  push_pointer(type);
}
function load_synopsis_wide(type=[]) {
  if (!document.getElementById("wide-synopses").hasChildNodes()) {
    while (!(type.includes(features[synopsis_pointer][1])) && !(type.length == 0)) {
      synopsis_pointer += 1;
    }
    var div = document.createElement('div');
    div.setAttribute("style", "margin: 25px 0 15px 0");
    div.setAttribute("id", "wide");
    document.getElementById("wide-synopses").appendChild(div);
    $("#wide").load(parent_folder_dictionary[features[synopsis_pointer][1]]+"/"+features[synopsis_pointer][0].replaceAll(" ","%20")+"/Synopsis%20Wide.html");
    synopsis_pointer += 1;
  }
  push_pointer(type);
}
function load_synopses_compact(number_of_synopses, type=[]) {
  var end_index = synopsis_pointer+number_of_synopses;
  synopsis_pointer += number_of_synopses;
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
      synopsis_pointer += 1;
    }
  }
  push_pointer(type);
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
    load_synopses(6,["ar"]);
  }
};