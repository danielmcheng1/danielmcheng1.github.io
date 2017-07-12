
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
 To Do
    Make this data structure better..
    Move to FLASK template 
        https://stackoverflow.com/questions/11178426/how-can-i-pass-data-from-flask-to-javascript-in-a-template
    TBDs in python apprentice module 
    
 */
 
 
 /*socket connection*/
var socket = io.connect('http://' + document.domain + ':' + location.port);
//socket.emit('human message', {"message": data['message']});


var sourceForTile;
socket.on ('begin play', function(data) {
    refreshBoard(data);
    
    //selecting/unselecting tiles
    $(".tileNotFixed").click(function () {
        if ($(this).hasClass('tileHuman')) {
            if ($(this).hasClass('tileUnselected')) {
                //untoggle any other tile that was selected 
                $(".tileSelected").not(this).toggleClass('tileUnselected tileSelected');
                //select this current tile 
                $(this).toggleClass('tileUnselected tileSelected');
            } else {
                $(this).toggleClass('tileUnselected tileSelected');
            };
            //$(this).toggleClass('tileUnselected tileSelected');
        };
    });
    
    //click to move tile
    $(".tileNotFixed").click(function(event) {
        event.stopPropagation(); //only select the topmost element
        var clicked = $(event.target);
        if (sourceForTile == undefined) {
            if (clicked.hasClass('tilePoints')) {
                if (clicked.parent().hasClass('tileNotFixed')) {
                    sourceForTile = clicked.parent();
                };
            } 
            else {
                sourceForTile = clicked;
            };
        };
    });
    
    //click to place tile
    $(".boardCell, .rackCell").click(function(event) {
        event.stopPropagation(); //only select the topmost element
        var clicked = $(event.target);
        if (sourceForTile != undefined) {
            if (clicked.hasClass('bonusOverlay')) {
                if (clicked.parent().hasClass('boardCell')) {
                    clicked.parent().append(sourceForTile);
                    clicked.remove();
                };
            }
            else if (clicked.hasClass('boardCell') || clicked.hasClass('rackCell')) {
                clicked.append(sourceForTile);
            };
            //sound effect 
            playSoundTileMoved();
            //unselect tile 
            $(".tileSelected").toggleClass('tileUnselected tileSelected');
            //reset source 
            sourceForTile = undefined;
        } 
    });
});

function refreshBoard(data) {
        
    var board = data;
    
    var BOARD_MAX_ROW = board.length;
    var BOARD_MAX_COL = board[0].length;
    var BOARD_MIN_ROW = 0;
    var BOARD_MIN_COL = 0;
    
    var table_whole = "";
    for (var i = 0; i < BOARD_MAX_ROW; i++) {
        var table_row = "<tr>";
        for (var j = 0; j < BOARD_MAX_COL; j++) {
            var table_cell = '';
            var tile_obj = board[i][j]["tile"];
            if (tile_obj != '') {
                var player_type = tile_obj["player_type"];
                var letter = tile_obj["letter"];
                var points = tile_obj["points"];
                tile_span = '<span class="tile tileFixed tileUnselected tile' + player_type + '">' + letter + '<sub class="tilePoints">' + points + '</sub></span>'; 
                table_cell = '<td class="boardCell noBonusFill" id=board_' + i + '_' + j + '>' + tile_span;         
            } 
            else {
                var bonus = board[i][j]["bonus"];
                if (bonus != '') {
                    bonusSpan = '<span class="bonusOverlay">' + bonus + ' Score</span>';
                    table_cell = '<td class="boardCell bonusFill' + bonus.replace(" ", "") + '" id=board_' + i + '_' + j + '>' + bonusSpan;
                } else {
                    table_cell = '<td class="boardCell noBonusFill" id=board_' + i + '_' + j + '>';  
                };
            };
            table_cell = table_cell + '</td>';
            table_row = table_row + table_cell;
        };
        table_row = table_row + "</tr>";
        table_whole = table_whole + table_row;
    };
    
    $("#board").empty();
    $("#board").append(table_whole);
};

function playSoundTileMoved() {    
    var audio = document.createElement("audio");
    audio.src = "static/sound/click2.mp3";
    audio.play();
};
/*
    document.body.onclick = function(evt) {
        var evt = window.event || evt;
        if (source != undefined) {
            evt.target.append(source);
            source = undefined;
        } 
        else {
            source = evt.target;
        };
    };
*/

/*
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
*/