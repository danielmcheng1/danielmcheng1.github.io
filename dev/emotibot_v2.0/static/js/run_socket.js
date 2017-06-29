/*socket connection*/
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
});
socket.on ('begin chat', append_bot_response)
socket.on ('bot message', append_bot_response)

function append_bot_response(data) {
    console.log("Received: " + data["message"]);
    
    $('<div class="shout_msg">' + 
          '<time>' + new Date().toLocaleTimeString() + '</time>' +
          '<span class = "username">' + "Bot" + '</span>' +
          '<span class = "message">' + data['message'] + '</span>' + 
      '</div>').appendTo('.message_box').fadeIn();
    
};


/*loading data into the chat box*/
$("#shout_message").keypress(function(evt) {
    if(evt.which == 13) {
        var iusername = $('#shout_username').val();
        var imessage = $('#shout_message').val();
        data = {'username':iusername, 'message':imessage};
       
        
        //append data into messagebox
        $('<div class="shout_msg">' + 
              '<time>' + new Date().toLocaleTimeString() + '</time>' +
              '<span class = "username">' + data['username'] + '</span>' +
              '<span class = "message">' + data['message'] + '</span>' + 
          '</div>').appendTo('.message_box').fadeIn();

        socket.emit('human message', {"message": data['message']})
        //keep scrolled to bottom of chat
        var scrolltoh = $('.message_box')[0].scrollHeight;
        $('.message_box').scrollTop(scrolltoh);
        
        //reset value of message box
        $('#shout_message').val('');
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

