
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



var sourceTile;
var sourceCell;
var placedTilesHuman;
    
//kick off the music 
//prevent these from being clicked until game has started 
$("#playMoveHuman").addClass("buttonClicked");
$("#exchangeTilesHuman").addClass("buttonClicked");
$("#passHuman").addClass("buttonClicked");
 
function postData(data) {
    return $.ajax({
        type: 'POST',
        url: $SCRIPT_ROOT + '/moveDoneHuman', //window.location.href,
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8'
    });
};

$("#restartGame").click (function(event) {
    if (!$(this).hasClass("buttonClicked")) {
        $(this).addClass("buttonClicked");
        postData({"Restart Game": "Y"}).done(handleData); 
    };
});

$(document).ready(function() {
    playBackgroundMusic();
    postData({}).done(handleData); 
});
    
    
function handleData(data) {
    refreshBoard(data);
    refreshPlacedTilesHuman(data);
    refreshRack(data, 'Human');
    refreshRack(data, 'Computer');
    refreshGameInfo(data);
    var board = data["board"];
    
    var soundEffectsDOM = document.getElementById("soundEffects"); //for tile placement, bag shuffling, etc.
    
    //once data has refreshed, allow player to restart game
    $("#restartGame").removeClass("buttonClicked");
    
    //once data has refreshed, allow player to send move 
    $("#playMoveHuman").removeClass("buttonClicked");
    $("#playMoveHuman").on('keypress click', function(event) {
        //enter key or mouse click 
        if (event.which === 13 || event.type === 'click') {
            if (!$(this).hasClass("buttonClicked")) {
                //socket.emit('moveDoneHuman', {"last_move": {"action": "Try Placing Tiles", "player": "Human", "detail": placedTilesHuman}});
                postData({"last_move": {"action": "Try Placing Tiles", "player": "Human", "detail": placedTilesHuman}}).done(handleData);
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
                //socket.emit('moveDoneHuman', {"last_move": {"action": "Try Exchanging Tiles", "player": "Human", "detail": toExchange}});
                postData({"last_move": {"action": "Try Exchanging Tiles", "player": "Human", "detail": toExchange}}).done(handleData);
                $(this).addClass("buttonClicked");
            };
        };
    });
    
    $("#passHuman").removeClass("buttonClicked");
    $("#passHuman").on('keypress click', function(event) {
        //enter key or mouse click 
        if (event.which === 13 || event.type === 'click') {
            if (!$(this).hasClass("buttonClicked")) {
                //socket.emit('moveDoneHuman', {"last_move": {"action": "Try Passing", "player": "Human", "detail": ""}});
                postData({"last_move": {"action": "Try Passing", "player": "Human", "detail": ""}}).done(handleData);
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
    
    //game info toggle 
    var gameInfo = document.getElementById('gameInfo');    
    var showGameInfo = document.getElementById("showGameInfo");
    var close = document.getElementById("closeGameInfo");
    showGameInfo.onclick = function() {
        gameInfo.style.display = "block";
    }
    close.onclick = function() {
        gameInfo.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target != gameInfo && event.target != showGameInfo) {
            gameInfo.style.display = "none";
        }
    };
    //toggleInstructions 
    var instructions = document.getElementById('instructions');
    var showInstructions = document.getElementById('showInstructions');
    var instructionsImage = document.getElementById('instructionsImage');
    instructionsImage.src = "../static/img/instructions.png";
    instructionsImage.alt = "Loading instructions...";
    window.onclick = function(event) {
        instructions.style.display = "none";
    };
    showInstructions.onclick = function() {
        instructions.style.display = "block";
    };
};
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
    var lastMove = data["lastMove"];        
    var lastMoveDetail = parseLastMove(lastMove);
    var gameInfo = data["gameInfo"];      
    var gameEndReason = gameInfo["gameEndReason"];
    var gameInfoDiv = document.getElementById("gameInfo");  
    
    if (gameInfo != undefined) {
        //show last move information = exception reason from Python if human made an illegal play
        $("#lastMove").text(lastMoveDetail);
        
        //show tiles left in bag
        $("#tilesLeft").text(parseTilesLeft(gameInfo["tilesLeft"]));
                
        //build the table of words played x score
        var table_whole = '' +
            '<tr class="wordsPlayedHeader">' + 
                '<td class="wordsPlayedHeaderCell">' + 
                'Your Move' + 
                '</td>' + 
                '<td class="wordsPlayedHeaderCell">' + 
                'Score' + 
                '</td>' + 
                '<td class="wordsPlayedHeaderCell">' + 
                '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ' +      
                '</td>' + 
                '<td class="wordsPlayedHeaderCell">' + 
                'Computer Move' + 
                '</td>' + 
                '<td class="wordsPlayedHeaderCell">' + 
                'Score' + 
                '</td>' + 
            '</tr>';
        ;
            
        var wordsPlayedComputer = gameInfo["wordsPlayedComputer"];
        var wordsPlayedHuman = gameInfo["wordsPlayedHuman"];
        for (var i = 0; i < Math.max(wordsPlayedComputer.length, wordsPlayedHuman.length); i++) {
            var wordHuman = parseWord(wordsPlayedHuman, i);
            var wordComputer = parseWord(wordsPlayedComputer, i);
            var scoreHuman = parseScore(wordsPlayedHuman, i);
            var scoreComputer = parseScore(wordsPlayedComputer, i);
            var table_row = '<tr class="wordsPlayedRow">' +
                                '<td class="wordsPlayedCell">' +
                                    wordHuman +
                                '</td>' +
                                '<td class="wordsPlayedCell">' +
                                    scoreHuman +
                                '</td>' +
                                '<td class="wordsPlayedCell">' +
                                    // dummy column
                                '</td>' +
                                '<td class="wordsPlayedCell">' +
                                    wordComputer +
                                '</td>' +
                                '<td class="wordsPlayedCell">' +
                                    scoreComputer +
                                '</td>' + 
                            '</tr>';
            table_whole = table_whole + table_row;
        };
        var table_row = '<tr class="wordsPlayedRowTotal">' +
                            '<td class="wordsPlayedCell">' +
                                // total row
                            '</td>' +
                            '<td class="wordsPlayedCell">' +
                                gameInfo["scoreHuman"] +
                            '</td>' +
                            '<td class="wordsPlayedCell">' +
                                // dummy column
                            '</td>' +
                            '<td class="wordsPlayedCell">' +
                                // total row
                            '</td>' +
                            '<td class="wordsPlayedCell">' +
                                gameInfo["scoreComputer"] +
                            '</td>' + 
                        '</tr>';
        table_whole = table_whole + table_row;
        
            
        $("#wordsPlayedTable").empty();
        $("#wordsPlayedTable").append(table_whole);
    };
    
    //decide whether to show this game info hover box
    if (lastMoveDetail != "" || gameEndReason != "") {
        gameInfoDiv.style.display = "block";
    }
    else {
        gameInfoDiv.style.display = "none";
    }
    
    if (gameEndReason != "") {
        $("#playMoveHuman").addClass("buttonClicked");
        $("#exchangeTilesHuman").addClass("buttonClicked");
        $("#passHuman").addClass("buttonClicked");
        $("#lastMove").text(gameEndReason);
    };    
};


function parseWord(wordsPlayed, index) {
    if (wordsPlayed[index] == undefined) {
        return "";
    }
    return wordsPlayed[index]["word"].join("");
};
function parseScore(wordsPlayed, index) {
    if (wordsPlayed[index] == undefined) {
        return "";
    }
    return wordsPlayed[index]["score"];
};
function parseTilesLeft(tilesLeft) {
    if (tilesLeft == undefined) 
        return "";
    if (tilesLeft == 1) 
        tileNoun = "tile";
    else 
        tileNoun = "tiles";
    return tilesLeft + " " + tileNoun + " left in the bag";
}
function parseLastMove(lastMove) {
    if (lastMove!= undefined) {
        //var detail = lastMove["action"] == "Made Illegal Move"? ": " + lastMove["detail"] : "";
        if (lastMove["action"].toUpperCase() == "MADE ILLEGAL MOVE") {
            return "Illegal Move! " + lastMove["detail"];
        };
    };
    return "";
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
    var audioPlaylist = ["background_waxcat", "background_completemusiccircle", "background_firefly", "background_newrain", "background_siesta", "background_oceanmist"]
    
    if (audioDOM.src == "") {
        //var audioDOM = document.createElement("audio");
        //audioDOM.setAttribute("id", "backgroundMusic");
        var startingSongId = Math.floor(Math.random() * (audioPlaylist.length));
        audioDOM.src = "static/sound/" + audioPlaylist[startingSongId] + ".mp3";
        audioDOM.volume = 0.7;
        audioDOM.load();
        audioDOM.play();
        audioDOM.addEventListener('ended', function() {
            var parsedSrc = audioDOM.src.match(/.*\/(.*)\.mp3/)[1] || "";
            var playlistIndex = audioPlaylist.indexOf(parsedSrc);
            var nextSong = audioPlaylist[(playlistIndex + 1) % audioPlaylist.length];
            audioDOM.src = "static/sound/" + nextSong + ".mp3";
            audioDOM.play();
        });
    };
};

return 


