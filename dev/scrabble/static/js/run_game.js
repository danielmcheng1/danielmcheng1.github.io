
BOARD_MIN_ROW = 0;
BOARD_MAX_ROW = 15;
BOARD_MIN_COL = 0;
BOARD_MAX_COL = 15;

var table_whole = "";
for (var i = 0; i <= BOARD_MAX_ROW; i++) {
    var table_row = "<tr>";
    for (var j = 0; j <= BOARD_MAX_COL; j++) {
        table_cell = '<td class=boardCells id=board_' + i + '_' + j + '</td>';
        table_row = table_row + table_cell;
    };
    table_row = table_row + "</tr>";
    table_whole = table_whole + table_row;
};
$("#board").append(table_whole)