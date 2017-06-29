/*socket connection*/
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    socket.emit('my event', {bot: 'Ellie', message: 'Initializing'});
    console.log('connected');
});
socket.on ('message', function(data)  { 
    console.log("Message: Received the following")
    console.log(data)
});
socket.on ('my emit', function(data)  { 
    console.log("Emit: Received the following")
    for (var key in data) {
        console.log(key, data[key])
    };
});
socket.on ('server originated', function(data)  { 
    console.log("server originated: Received the following")
    for (var key in data) {
        console.log(key, data[key])
    };
});

/*loading data into the chat box*/


$("#shout_message").keypress(function(evt) {
    if(evt.which == 13) {
            var iusername = $('#shout_username').val();
            var imessage = $('#shout_message').val();
            post_data = {'username':iusername, 'message':imessage};
           
            data = $.map(post_data, function(value, index) {
                return [value];
            });
            
            //append data into messagebox with jQuery fade effect!
            
            $('<div class="shout_msg">' + 
                  '<time>' + new Date().toLocaleTimeString() + '</time>' +
                  '<span class = "username">' + post_data['username'] + '</span>' +
                  '<span class = "message">' + post_data["message"] + '</span>' + 
              '</div>').appendTo('.message_box').fadeIn();
  
            //keep scrolled to bottom of chat!
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
    }else{
        $(".header div").attr('class', 'close_btn');
    }
});

