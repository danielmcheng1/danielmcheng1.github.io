/*socket connection*/
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on ('connect', function(data) {
    appendMessageBox('ELIANA', 1)
    appendMessageBox('ANA', 2)
    appendMessageBox('OLGA', 3);
        
    socket.on ('begin chat', function(data) {
        console.log('begin', data);
        append_to_chat_box(data);
        refresh_charts(data);
    });
    socket.on ('bot message', function(data) {
        console.log('message', data);
        append_to_chat_box(data);
        refresh_charts(data);
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
        //get CSS display state of .toggle_chat element
        var toggleState = $('.toggle_chat').css('display');
        //use toggleState var to change close/open icon image
        if(toggleState == 'none') {
            $(".chat_header div").attr('class', 'close_btn');
        } else {
            $(".chat_header div").attr('class', 'open_btn');
        };
        //toggle show/hide chat box (.next to restrict to the current chat window)
        $(this).next('.toggle_chat').slideToggle();
    });
});
function appendMessageBox(username, num_message_boxes) {
    //var num_message_boxes = 1;
    var this_message_box = 
        '<div class="chat_box right_' + num_message_boxes + '">' + 
            '<div class="chat_header">' + username.toProperCase()  + '<div class="close_btn">&nbsp;</div></div>' + 
                '<div class="toggle_chat">' + 
                '<div class="message_box" id = "message_box_' + username + '"></div>' + 
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
    var scrolltoh = $('#message_box+' + requested_bot)[0].scrollHeight;
    $('#message_box_' + requested_bot).scrollTop(scrolltoh);
};

String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/, function(token) {
        return token.charAt(0).toUpperCase() + token.substr(1).toLowerCase();
    });
};
    