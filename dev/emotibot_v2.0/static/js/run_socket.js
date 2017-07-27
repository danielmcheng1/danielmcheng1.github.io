/*socket connection*/
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on ('begin chat', function(data) {
    append_to_chat_box(data);
    refresh_charts(data);
});
socket.on ('bot message', function(data) {
    append_to_chat_box(data);
    refresh_charts(data);
});

function append_to_chat_box(data) {    
    $('<div class="shout_msg">' + 
          '<span class = "username">' + data['username'] +
            '<time>' + new Date().toLocaleTimeString() + '</time>' +
          '</span>' +
          '<span class = "message">' + data['message'] + '</span>' + 
      '</div>').appendTo('.message_box').fadeIn();
    
    scroll_message_box();
};
function refresh_charts(data) {
    if (data['emotions'])
        wrapper_refreshEmotionsChart(data['emotions']);
    if (data['keywords'])
        wrapper_refreshKeywordsChart(data['keywords']);
    if (data['history'])
        wrapper_refreshChatHistory(data['history']);
};
    

//keep scrolled to bottom of chat
function scroll_message_box() {
    var scrolltoh = $('.message_box')[0].scrollHeight;
    $('.message_box').scrollTop(scrolltoh);
};

/*loading data into the chat box*/
$("#shout_message").keypress(function(evt) {
    if(evt.which == 13) {
        data = {'message': $('#shout_message').val(), 'username': $('#shout_username').val() || "You"};        
        append_to_chat_box(data);
        
        $('#shout_message').val('');
        
        //for testing 
        //wrapper_refreshEmotionsChart({"anger": 0.1, "fear": 0.2, "joy": 0.3, "sadness": 0.4, "surprise": 0.5});

        socket.emit('human message', {"message": data['message']});
    }
});

//toggle hide/show shout box
$(".chat_header").click(function (e) {
    //get CSS display state of .toggle_chat element
    var toggleState = $('.toggle_chat').css('display');
    console.log(toggleState)
    //use toggleState var to change close/open icon image
    if(toggleState == 'none') {
        $(".chat_header div").attr('class', 'close_btn');
    } else {
        $(".chat_header div").attr('class', 'open_btn');
    };
    //toggle show/hide chat box (.next to restrict to the current chat window)
    $(this).next('.toggle_chat').slideToggle();
});

