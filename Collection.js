var pieces;
var pieces_index = -1;

function set_pieces(pieces_list) {
  pieces = pieces_list;
}

function change_piece(direction) {
  pieces_index = (pieces_index+{"right":1,"left":-1}[direction]+pieces.length) % pieces.length;
  $.get("/Art/"+pieces[pieces_index]+"/Linked%20Piece.html", function(data) {
    var piece = document.createElement('div');
    piece.innerHTML = data.trim();
    piece.firstElementChild.firstElementChild.setAttribute("class", "collection-image");
    $("a").remove(".feature-link");
    $(".collection-container").append(piece); 
  }).fail(function() {
    change_piece(direction);
  });
}