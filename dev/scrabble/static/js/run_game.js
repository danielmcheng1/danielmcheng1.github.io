
BOARD_MIN_ROW = 0;
BOARD_MAX_ROW = 15;
BOARD_MIN_COL = 0;
BOARD_MAX_COL = 15;
BOARD_CENTER_ROW = 7;
BOARD_CENTER_COL = 7;
var INPUT_BOARD_TILES = [
    [ 'T', 'H', 'E', '', 'Q', 'U', 'I', 'C', 'K', '', '', '', '', '', ''],
    ['B', 'R', 'O', 'W', 'N', '', 'F', 'O', 'X', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    
    
    ['', 'J', 'U', 'M', 'P', 'E', 'D', '', 'O', 'V', 'E', 'R', '', '', ''],
    
    ['', '', '', 'T', 'H', 'E', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', 'L', 'A', 'Z', 'Y'],
    ['', '', '', '', '', '', '', 'S', 'L', 'E', 'E', 'P', 'I', 'N', 'G'],
    ['', '', '', '', '', 'D', 'O', 'G', 'S', '', '', '', '', '', '']
];
var table_whole = "";
for (var i = 0; i < BOARD_MAX_ROW; i++) {
    var table_row = "<tr>";
    for (var j = 0; j < BOARD_MAX_COL; j++) {
        var table_cell = '<td class=boardCells id=board_' + i + '_' + j + '>';
        console.log(INPUT_BOARD_TILES, i , j)
        var letter = INPUT_BOARD_TILES[i][j];
        if (letter != '') {
            if (j % 2) 
                var player = 'Computer';
            else 
                var player = 'Human';
            tile = '<span class="tileOnBoard tileUnselected tile' + player + '">' + letter + '<sub class="tilePoints">1</sub></span>'; 
            table_cell = table_cell + tile;         
        };
        table_cell = table_cell + '</td>';
        table_row = table_row + table_cell;
    };
    table_row = table_row + "</tr>";
    table_whole = table_whole + table_row;
};
$("#board").append(table_whole);

$(".tileOnBoard").click(function () {
    if ($(this).hasClass('tileHuman'))
        $(this).toggleClass('tileUnselected tileSelected');
});