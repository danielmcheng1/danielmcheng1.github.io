
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
    fix game bugs 
        why going twice? probably sending message twice?
        too many tiles drawn at beginning? 
        some words not in dict? 
        handl eerrors 
        exchange rack
    show game info
    other 
        add delay to computer move
        instructions while waiting
        confident enough to show tiles
        refreshing page/starting game over
        https://www.soundsnap.com/tags/scrabble Scrabble game tile down 2 and Scrabble game with hand in bag
    Make this data structure better..
    Move to FLASK template 
        https://stackoverflow.com/questions/11178426/how-can-i-pass-data-from-flask-to-javascript-in-a-template
    TBDs in python apprentice module 
        '''
    #class has to also flag who just played the tile....
    #clean up functions --should really recreate everything in the class --
    #capitalize classes
    #make move each time -- 
        computer_player = scrabble_game_play.play_order[1]
    score = self.board.make_human_move(input_row, input_col, input_dir, input_word, player.rack)
    scrabble_board_wrapper = [[{"bonus": map_bonus_to_view(scrabble_board.board[row][col]), \
                                "tile": map_tile_to_view(scrabble_board.board[row][col], 'Human', scrabble_score_dict)} \
                                for col in range(MAX_COL)] \
                                for row in range(MAX_ROW)] 
   
    TBD add validatoin 
    //TBD try removing table in rack --spacing changes
    //bonus text not centered 
    '''
 */
 
 
 /*socket connection*/
var socket = io.connect('http://' + document.domain + ':' + location.port);


var sourceTile;
var sourceCell;
var placedTilesHuman;
    
$("#playMoveHuman").addClass("buttonClicked");
$("#swapTilesHuman").addClass("buttonClicked");
$("#startGame").click (function(event) {
    if (!$(this).hasClass("buttonClicked")) {
        console.log("starting game...");
        socket.emit('moveDoneHuman', {});  
        $(this).addClass("buttonClicked");
    };
});
socket.on('moveDoneComputer', function(data) {
    console.log(data);
    
    refreshBoard(data);
    refreshPlacedTilesHuman(data);
    refreshRack(data, 'Human');
    refreshRack(data, 'Computer');
    
    //create audio element
    var soundEffects = document.createElement("audio");
    
    $("#playMoveHuman").removeClass("buttonClicked");
    $("#playMoveHuman").click (function(event) {
        if (!$(this).hasClass("buttonClicked")) {
            console.log("emitting move", placedTilesHuman);
            socket.emit('moveDoneHuman', {"placedTilesHuman": placedTilesHuman});
            $(this).addClass("buttonClicked");
        };
    });
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
        if (clicked.hasClass('tilePoints')) {
            if (clicked.parent().hasClass('tileNotFixed')) {
                sourceTile = clicked.parent();
            };
        } 
        else {
            sourceTile = clicked;
        };
        sourceCell = sourceTile.parent();
    });
    
    //click to place tile
    $(".boardCell, .rackCell").click(function(event) {
        event.stopPropagation(); //only select the topmost element
        var clicked = $(event.target);
        var targetCell;
        if (sourceTile != undefined) {
            if (clicked.hasClass('bonusOverlay') && clicked.parent().hasClass('boardCell')) {
                targetCell = clicked.parent();
                clicked.remove();
            }
            else if (clicked.hasClass('boardCell') || clicked.hasClass('rackCell')) {
                targetCell = clicked;
            };
            if (targetCell) {
                //sound effect 
                playSoundTileMoved(soundEffects);
                
                //push tile onto cell 
                targetCell.append(sourceTile);
                
                //redraw the bonus in the source cell since tile is no longer covering the source cell
                var targetId = targetCell.attr("id");
                var sourceId = sourceCell.attr("id");
                if ($("#" + sourceId).hasClass("boardCell")) {
                    var sourceIdParsed = parseIntoRowCol(sourceId);
                    var targetIdParsed = parseIntoRowCol(targetId);
                    var bonus = data["board"][sourceIdParsed["row"]][sourceIdParsed["col"]];
                    if (bonus != '') {
                        bonusSpan = '<span class="bonusOverlay">' + bonus + ' Score</span>';
                        $("#" + sourceId).append($(bonusSpan));
                    };
                };
                
                //save the row, col of the target 
                updatePlacedTilesHuman(sourceId, targetId);
                //unselect tile 
                $(".tileSelected").toggleClass('tileUnselected tileSelected');
                
                //reset source 
                sourceTile = undefined;
            };
        } 
    });
});

function parseIntoRowCol(id) {
    var regexResult = /.*_([0-9]+)_([0-9]+)/.exec(id);
    var rv;
    if (regexResult) {
        rv = {};
        rv["row"] = regexResult[1];
        rv["col"] = regexResult[2];
    }
    return rv;
};

function pullLetterAtCellId(id) {
    //.text() returns letter + points so substring to just the first character
    return $("#" + id).find(".tile").text().charAt(0);
    //return (document.getElementById(targetId).childNodes);
};

function updatePlacedTilesHuman(sourceId, targetId) {
    if ($("#" + targetId).hasClass("boardCell")) {
        var idParsed = parseIntoRowCol(targetId);
        var letter = pullLetterAtCellId(targetId);
        //push target onto list of placed tiles
        placedTilesHuman[idParsed["row"]][idParsed["col"]] = letter;                        
    };
    if ($("#" + sourceId).hasClass("boardCell")) {
        var idParsed = parseIntoRowCol(sourceId);
        placedTilesHuman[idParsed["row"]][idParsed["col"]] = "";
        //var existingIndex = placedTilesHuman.findIndex(function(elem) {
        //    return elem["row"] == idParsed["row"] && elem["col"] == idParsed["col"];
        //});
        //placedTilesHuman.splice(existingIndex, 1)
    };
};

function refreshRack(data, player) {
    var tiles = data["rack" + player];
    var rack = "<table><tr>";
    for (var i = 0; i < tiles.length; i++) {
        var letter = tiles[i];
        var points = 3;
        var span = '<span class = "tile tileNotFixed tileUnselected tile' + player + '">' + letter + '<sub class="tilePoints">' + points + '</sub></span';
        var cell = '<td class = "rackCell">' + span + '</td>';
        rack = rack + cell;
    };
    rack = rack + "</tr></table>";
    $("#rack" + player).empty();
    $("#rack" + player).append(rack);
};

function refreshPlacedTilesHuman(data) {
    placedTilesHuman = [];
    for (var i = 0; i < data["board"].length; i++) {
        var thisRow = [];
        for (var j = 0; j < data["board"][0].length; j++) {
            thisRow.push("");
        };
        placedTilesHuman.push(thisRow);
    };
};
function refreshBoard(data) {
    var tiles = data["tiles"];
    var board = data["board"];
    
    var BOARD_MAX_ROW = board.length;
    var BOARD_MAX_COL = board[0].length;
    var BOARD_MIN_ROW = 0;
    var BOARD_MIN_COL = 0;
    
    var table_whole = "";
    for (var i = 0; i < BOARD_MAX_ROW; i++) {
        var table_row = "<tr>";
        for (var j = 0; j < BOARD_MAX_COL; j++) {
            var table_cell = '';
            var tile_obj = tiles[i][j];
            if (tile_obj != '') {
                var player_type = tile_obj["player_type"];
                var letter = tile_obj["letter"];
                var points = tile_obj["points"];
                tile_span = '<span class="tile tileFixed tileUnselected tile' + player_type + '">' + letter + '<sub class="tilePoints">' + points + '</sub></span>'; 
                table_cell = '<td class="boardCell noBonusFill" id=boardCell_' + i + '_' + j + '>' + tile_span;         
            } 
            else {
                var bonus = board[i][j];
                if (bonus != '') {
                    bonusSpan = '<span class="bonusOverlay">' + bonus + ' Score</span>';
                    table_cell = '<td class="boardCell bonusFill' + bonus.replace(" ", "") + '" id=board_' + i + '_' + j + '>' + bonusSpan;
                } else {
                    table_cell = '<td class="boardCell noBonusFill" id=boardCell_' + i + '_' + j + '>';  
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

function playSoundTileMoved(audioDOM) {    
    audioDOM.src = "static/sound/click2.mp3";
    audioDOM.load();
    audioDOM.play();
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