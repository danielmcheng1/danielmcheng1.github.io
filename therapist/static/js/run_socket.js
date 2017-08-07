/*socket connection*/
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on ('connect', function(data) {
    //create the chat boxes for each therapist persona 
    $("#messages_boxes_start").empty();
    appendMessageBox('ELIANA');
    appendMessageBox('ANA');
    appendMessageBox('OLGA');
    
    //start these off minimized 
    toggleChat('ANA');
    toggleChat('OLGA');
    
    //initiate Eliana chat 
    socket.emit('begin chat', 'ELIANA');
    
    //background music 
    var backgroundDOM = document.createElement("audio");
    playBackgroundMusic(backgroundDOM);
    
    socket.on('bot message', function(data) {
        //add some delay to make conversation more realistic (particularly for the non-ELIANA bots which don't require any API calls 
        var waitSeconds = Math.random() * (data["requested_bot"] == 'ELIANA' ? 0.5 : 1.5);
        setTimeout(function(){
            append_to_chat_box(data);
            refresh_charts(data);
        }, waitSeconds * 1000);
    });
    /*loading data into the chat box*/
    $("input[name=chat_message]").keypress(function(evt) {
        if(evt.which == 13) {
            var this_id = $(this).attr("id");
            var requested_bot = this_id.match(/chat_message_(.*)/)[1];
            var message = $('#' + this_id).val();
            var username = $('#chat_username_' + requested_bot).val() || "You";   
            var data = {"message": message, "username": username, "requested_bot": requested_bot}

            append_to_chat_box(data);
            
            $('#' + this_id).val('');
            socket.emit('human message', data);
            
            //for testing 
            //wrapper_refreshEmotionsChart({"anger": 0.1, "fear": 0.2, "joy": 0.3, "sadness": 0.4, "surprise": 0.5});

        }
    });

    //toggle hide/show chat box
    $(".chat_header").click(function (e) {
        var this_id = $(this).attr("id");
        var requested_bot = this_id.match(/chat_header_(.*)/)[1];
        toggleChat(requested_bot);
        if (!$("#" + this_id).hasClass("chat_began")) {
            socket.emit('begin chat', requested_bot);
            $("#" + this_id).addClass("chat_began");
        };
        
    });
});
/*
jQuery.fn.extend({
    function_name: function() {
    }
});
*/
function appendMessageBox(username) {
    var this_message_box = 
        '<div class="chat_box offset_' + ($(".chat_box").length + 1) + '">' + 
            '<div class="chat_header" id="chat_header_' + username + '">' + 
                username.toProperCase() + 
                '<div class="close_btn" id="chat_button_' + username + '">&nbsp;</div>' +
            '</div>' + 
                    '<div class="toggle_chat" id="toggle_chat_' + username + '">' + 
                    '<div class="message_box" id="message_box_' + username + '"></div>' + 
                    '<div class="user_info">' +
                        '<input name="chat_username" id="chat_username_' + username + '" type="text" placeholder="Your Name" />' + 
                        '<input name="chat_message" id="chat_message_' + username + '" type="text" placeholder="Type Message Hit Enter"/> ' +
                    '</div>' +
            '</div>' +
        '</div>';

    $("#messages_boxes_start").append(this_message_box);
  
};

function refresh_charts(data) {
    if (data['emotions'])
        wrapper_refreshEmotionsChart(data['emotions']);
    if (data['keywords'])
        wrapper_refreshKeywordsChart(data['keywords']);
    if (data['history'])
        wrapper_refreshChatHistory(data['history']);
};
    


function append_to_chat_box(data) {    
    var requested_bot = data['requested_bot'];
    var message = data['message'];
    var username = data['username'];
    $('<div class="chat_msg">' + 
          '<span class = "username">' + username.toProperCase() +
            '<time>' + new Date().toLocaleTimeString() + '</time>' +
          '</span>' +
          '<span class = "message">' + message + '</span>' + 
      '</div>').appendTo('#message_box_' + requested_bot).fadeIn();
    
    scroll_message_box(requested_bot);
};
//keep scrolled to bottom of chat
function scroll_message_box(requested_bot) {
    var scrolltoh = $('#message_box_' + requested_bot)[0].scrollHeight;
    $('#message_box_' + requested_bot).scrollTop(scrolltoh);
};

function toggleChat(requested_bot) {
    $("#toggle_chat_" + requested_bot).slideToggle();
    $("#chat_button_" + requested_bot).toggleClass('open_btn close_btn');
} 
   
/********************************/
function playBackgroundMusic(audioDOM) {
    audioDOM.src = "static/sound/background.mp3";
    audioDOM.load();
    audioDOM.play();
    audioDOM.addEventListener('ended', function() {
        audioDOM.play();
    });
};

/****************************/
String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/, function(token) {
        return token.charAt(0).toUpperCase() + token.substr(1).toLowerCase();
    });
};
    