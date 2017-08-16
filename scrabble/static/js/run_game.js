
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
   logging
        why randomly shifts letters/wrong click and place e.g. triple word @bottom
            more responsive if child inherits parent
        start game over/not actually ending 
        add delay to computer move
        instructions while waiting
            say comop confident enough to show tile
        https://www.soundsnap.com/tags/scrabble Scrabble game tile down 2 and Scrabble game with hand in bag
    Make this data structure better..
    naming conventions
    Move to FLASK template 
        https://stackoverflow.com/questions/11178426/how-can-i-pass-data-from-flask-to-javascript-in-a-template
    improve error handling 
    TBDs in python apprentice module 
        '''
    scrabble move class ? 
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
    
//kick off the music 
//prevent these from being clicked until game has started 
$("#playMoveHuman").addClass("buttonClicked");
$("#exchangeTilesHuman").addClass("buttonClicked");
$("#passHuman").addClass("buttonClicked");
 
function postData() {
    return $.ajax({
            type: 'POST',
            url: $SCRIPT_ROOT + '/_add_numbers', //window.location.href,
            data: JSON.stringify({a: 1}),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8'
    });
};
function handleData(data) {
    alert('Received from server: ' + data);
};
$("#startGame").click (function(event) {
    postData().done(handleData);
})
/*
$("#startGame").click (function(event) {
    if (!$(this).hasClass("buttonClicked")) {
        playBackgroundMusic();
        socket.emit('moveDoneHuman', {});  
        $(this).addClass("buttonClicked");
    };
});
*/
socket.on('moveDoneComputer', function(data) {
    refreshBoard(data);
    refreshPlacedTilesHuman(data);
    refreshRack(data, 'Human');
    refreshRack(data, 'Computer');
    refreshLastMove(data);
    refreshGameInfo(data);
    var board = data["board"];
    
    var soundEffectsDOM = document.createElement("audio"); //for tile placement, bag shuffling, etc.
    
    //once data has refreshed, allow player to send move 
    $("#playMoveHuman").removeClass("buttonClicked");
    $("#playMoveHuman").on('keypress click', function(event) {
        //enter key or mouse click 
        if (event.which === 13 || event.type === 'click') {
            if (!$(this).hasClass("buttonClicked")) {
                socket.emit('moveDoneHuman', {"last_move": {"action": "Try Placing Tiles", "player": "Human", "detail": placedTilesHuman}});
                $(this).addClass("buttonClicked");
            };
        };
    });
    
    $("#exchangeTilesHuman").removeClass("buttonClicked");
    $("#exchangeTilesHuman").on('keypress click', function(event) {
        //enter key or mouse click 
        if (event.which === 13 || event.type === 'click') {
            if (!$(this).hasClass("buttonClicked")) {
                var toExchange = $(".exchangeCell").map(function(index, elem) {
                    if ($(this).text() != "") 
                        return  $(this).text()[0]; 
                    else 
                        return $(this).text();
                }).filter(function(index, elem) {
                    return elem != "";
                }).toArray();
                socket.emit('moveDoneHuman', {"last_move": {"action": "Try Exchanging Tiles", "player": "Human", "detail": toExchange}});
                $(this).addClass("buttonClicked");
            };
        };
    });
    
    $("#passHuman").removeClass("buttonClicked");
    $("#passHuman").on('keypress click', function(event) {
        //enter key or mouse click 
        if (event.which === 13 || event.type === 'click') {
            if (!$(this).hasClass("buttonClicked")) {
                socket.emit('moveDoneHuman', {"last_move": {"action": "Try Passing", "player": "Human", "detail": ""}});
                $(this).addClass("buttonClicked");                    
            };            
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
    $(".boardCell, .rackCell, .exchangeCell").click(function(event) {
        event.stopPropagation(); //only select the topmost element
        var clicked = $(event.target);
        var targetCell;
        if (sourceTile != undefined) {
            if (clicked.hasClass('bonusOverlay') && clicked.parent().hasClass('boardCell')) {
                targetCell = clicked.parent();
                clicked.remove();
            }
            else if (clicked.hasClass('boardCell') || clicked.hasClass('rackCell') || clicked.hasClass('exchangeCell')) {
                targetCell = clicked;
            };
            if (targetCell) {
                //sound effect 
                playSoundTileMoved(soundEffectsDOM);
                
                //push tile onto cell 
                targetCell.append(sourceTile);
                
                //redraw the bonus in the source cell since tile is no longer covering the source cell
                var targetId = targetCell.attr("id");
                var sourceId = sourceCell.attr("id");
                if ($("#" + sourceId).hasClass("boardCell")) {
                    var sourceIdParsed = parseIntoRowCol(sourceId);
                    var targetIdParsed = parseIntoRowCol(targetId);
                    var bonus = board[sourceIdParsed["row"]][sourceIdParsed["col"]];
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
    };
};

function refreshRack(data, player) {
    var tiles = data["rack" + player];
    var rack = "<table><tr>";
    //rack tiles 
    for (var i = 0; i < tiles.length; i++) {
        var letter = tiles[i]["letter"];
        var points = tiles[i]["points"];
        var span = '<span class = "tile tileNotFixed tileUnselected tile' + player + '">' + letter + '<sub class="tilePoints">' + points + '</sub></span';
        var cell = '<td class = "rackCell rackCell' + player + '">' + span + '</td>';
        rack = rack + cell;
    };
    
    //add in slots for exchanging tiles;
    if (player === "Human") {
        for (var i = 0; i < tiles.length; i++) {
            var exchange = '<td class = "exchangeCell"></td>';
            rack = rack + exchange;
        };
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

function refreshGameInfo(data) {
    var gameInfo = data["gameInfo"];          
    if (gameInfo != undefined) {
        $("#scoreComputer").text("Computer Score: " + gameInfo["scoreComputer"] + " points");
        $("#scoreHuman").text("Human Score: " + gameInfo["scoreHuman"] + " points");
        $("#tilesLeft").text("Tiles Left: " + gameInfo["tilesLeft"] + " tiles");
        
        refreshWordsPlayed("wordsPlayedComputer", gameInfo["wordsPlayedComputer"], "Computer");
        refreshWordsPlayed("wordsPlayedHuman", gameInfo["wordsPlayedHuman"], "Human");
        
        console.log(gameInfo)
        var gameEndReason = gameInfo["gameEndReason"] 
        if (gameEndReason != "") {
            $("#playMoveHuman").addClass("buttonClicked");
            $("#exchangeTilesHuman").addClass("buttonClicked");
            $("#passHuman").addClass("buttonClicked");
            $("#gameEndReason").text(gameEndReason);
        };
    };
};
function refreshWordsPlayed(id, wordsPlayed, player) {
    $("#" + id).empty();
    if (wordsPlayed.length == 0) 
        return;
    var table_whole = "<table>";
    for (var i = 0; i < wordsPlayed.length; i++) {
        var table_row = "<tr>";
        var table_cells = "<td>    " + wordsPlayed[i]["word"].join("") + "</td><td>" + wordsPlayed[i]["score"] + "</td>";
        table_row = table_row + table_cells;
        table_whole = table_whole + table_row;
    };
    table_whole = table_whole + "</table>";
    $("#" + id).append("Words Played by " + player + table_whole);
};

function refreshLastMove(data) {
    $("#lastMove").text(function () {
        var lastMove = data["lastMove"]
        if (lastMove!= undefined) {
            var detail = lastMove["action"] == "Made Illegal Move"? ": " + lastMove["detail"] : "";
            return lastMove["player"] + " " + lastMove["action"].toLowerCase() + detail;
        }
        else {
            return "";
        };
    });
};

function playSoundTileMoved(audioDOM) {    
    audioDOM.src = "static/sound/click2.mp3";
    audioDOM.volume = 1;
    audioDOM.load();
    audioDOM.play();
};
function playBackgroundMusic() {
    //check if exists because Flask will re-render each time
    var audioDOM = document.getElementById("backgroundMusic");
    if (audioDOM == null) {
        var audioDOM = document.createElement("audio");
        audioDOM.setAttribute("id", "backgroundMuisc");
        audioDOM.src = "static/sound/background_jazz.mp3";
        audioDOM.volume = 0.7;
        audioDOM.load();
        audioDOM.play();
        audioDOM.addEventListener('ended', function() {
            var parsedSrc = audioDOM.src.match(/.*\/(.*)\.mp3/)[1] || "";
            audioDOM.src = (parsedSrc == "background_jazz"? "static/sound/background_normal.mp3" : "static/sound/background_jazz.mp3");
            audioDOM.play();
        });
    };
};