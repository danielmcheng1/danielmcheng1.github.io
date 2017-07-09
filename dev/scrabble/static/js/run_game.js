
/*
DATA STRUCTURES
       Need to return:
    Players 
        self.name = name
        self.is_human = is_human
        self.rack = []  
        self.running_score = 0
        self.words_played = []
    Board State
        two-dimensional array representing board
        for each cell in board:
            "cell" object:
                .tile 
                    .letter 
                    .points
                    .player
                .bonus 
             if blank then attribute is N/A
     
 */
 /*socket connection*/
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on ('begin play', function(data) {
    console.log(data);
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
            var table_cell = '';
            var letter = INPUT_BOARD_TILES[i][j];
            if (letter != '') {
                if (j % 2) 
                    var player = 'Computer';
                else 
                    var player = 'Human';
                tile = '<span class="tileOnBoard tileUnselected tile' + player + '">' + letter + '<sub class="tilePoints">1</sub></span>'; 
                table_cell = '<td class="boardCell noBonusFill" id=board_' + i + '_' + j + '>' + tile;         
            } 
            else {
                var bonus = "";
                if (j == BOARD_MAX_COL - 1) {
                    if (i == 1) bonus = "Triple Word";
                    else if (i == 3) bonus = "Double Word";
                    else if (i == 5) bonus = "Triple Letter";
                    else if (i == 7) bonus = "Double Letter";
                };
                if (bonus != '') {
                    bonusSpan = '<span class="bonusOverlay">' + bonus + ' Score</span>';
                    table_cell = '<td class="boardCell bonusFill' + bonus.replace(" ", "") + '" id=board_' + i + '_' + j + '>' + bonusSpan;
                } else {
                    table_cell = '<td class="boardCell noBonusFill" id=board_' + i + '_' + j + '>';  
                };
                
                //table_cell = '<td class="boardCell noBonusFill" id=board_' + i + '_' + j + '>';
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
});
