
BOARD_MIN_ROW = 0;
BOARD_MAX_ROW = 15;
BOARD_MIN_COL = 0;
BOARD_MAX_COL = 15;
BOARD_CENTER_ROW = 7;
BOARD_CENTER_COL = 7;

var table_whole = "";
for (var i = 0; i <= BOARD_MAX_ROW; i++) {
    var table_row = "<tr>";
    for (var j = 0; j <= BOARD_MAX_COL; j++) {
        var table_cell = '<td class=boardCells id=board_' + i + '_' + j + '>';
        if ((i == 1 || i == 5 || i == 9) && (j == 1 || j == 3 || j == 11)) {
            var tile = '<span class="tileOnBoard tileComputer">S<sub class="tilePoints">1</sub></span>'  
            table_cell = table_cell + tile          
        };
        table_cell = table_cell + '</td>';
        table_row = table_row + table_cell;
    };
    table_row = table_row + "</tr>";
    table_whole = table_whole + table_row;
};
$("#board").append(table_whole)