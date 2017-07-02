/*socket connection*/
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
});
socket.on ('begin chat', append_to_chat_box)
socket.on ('bot message', append_to_chat_box)

function append_to_chat_box(data) {    
    $('<div class="shout_msg">' + 
          '<span class = "username">' + data['username'] +
            '<time>' + new Date().toLocaleTimeString() + '</time>' +
          '</span>' +
          '<span class = "message">' + data['message'] + '</span>' + 
      '</div>').appendTo('.message_box').fadeIn();
    
    scroll_message_box();
    if (data['emotions'])
        refreshChartData_EmotionsWrapper(data['emotions']);
};

//keep scrolled to bottom of chat
function scroll_message_box() {
    var scrolltoh = $('.message_box')[0].scrollHeight;
    $('.message_box').scrollTop(scrolltoh);
};

/*loading data into the chat box*/
$("#shout_message").keypress(function(evt) {
    if(evt.which == 13) {
        var iusername = $('#shout_username').val() || "You";
        var imessage = $('#shout_message').val();
        
        data = {'username':iusername, 'message':imessage};        
        append_to_chat_box(data);
        
        $('#shout_message').val('');
        
        //refreshChartData_EmotionsWrapper({"anger": 0.1, "fear": 0.2, "joy": 0.3, "sadness": 0.4, "surprise": 0.5});
        socket.emit('human message', {"message": data['message']});
    }
});

//toggle hide/show shout box
$(".close_btn").click(function (e) {
    //get CSS display state of .toggle_chat element
    var toggleState = $('.toggle_chat').css('display');

    //toggle show/hide chat box
    $('.toggle_chat').slideToggle();
    
    //use toggleState var to change close/open icon image
    if(toggleState == 'block')
    {
        $(".header div").attr('class', 'open_btn');
    } else{
        $(".header div").attr('class', 'close_btn');
    }
});

