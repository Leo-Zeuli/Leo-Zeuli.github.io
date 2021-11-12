var features = [["Bored to Death S1","r"],["Texas Chainsaw Massacre","a"],["Blade Runner 2049","a"],["Loki","r"]];
var features_loaded = new Array(features.length).fill(false);

var synopsis_pointer = 0;

function load_synopses(number_of_synopses,r_or_a=null) {
  var end_index = synopsis_pointer+number_of_synopses;
  synopsis_pointer += number_of_synopses;
  for (let i = end_index-number_of_synopses; i < Math.min(end_index,features.length); i++) {
    if ((r_or_a == null) || (features[i][1] == r_or_a)) {
      $.get("Features/"+features[i][0]+"/Synopsis.html", function(data) {
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
        load_synopses(1, r_or_a);
      });
    } else {
      end_index += 1;
    }
  }
}
function load_synopsis_wide(r_or_a=null) {
  if (!document.getElementById("wide-synopses").hasChildNodes()) {
    var div = document.createElement('div');
    div.setAttribute("style", "margin: 25px 0 25px 0");
    div.setAttribute("id", "wide");
    document.getElementById("wide-synopses").appendChild(div);
    $("#wide").load("Features/"+features[synopsis_pointer][0].replaceAll(" ","%20")+"/Synopsis%20Wide.html");
    synopsis_pointer += 1;
  }
}
function load_synopses_compact(number_of_synopses,r_or_a=null) {
  var end_index = synopsis_pointer+number_of_synopses;
  synopsis_pointer += number_of_synopses;
  for (let i = end_index-number_of_synopses; i < Math.min(end_index,features.length); i++) {
    $.get("Features/"+features[i][0]+"/Synopsis%20Compact.html", function(data) {
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
  }
}

function load_more(source) {
  if (source == "index") {
    load_synopsis_wide();
    load_synopses_compact(9);
  } else if (source == "reviews") {
    load_synopses(6,"r");
  } else if (source == "analyses") {
    load_synopses(6,"a");
  } else if (source == "features") {
    load_synopses(6);
  }
};