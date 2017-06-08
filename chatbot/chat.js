
/*global variables to access API.AI*/

var accessToken = "86bbaa261369454894e364da26cbebe1",
    baseUrl = "https://api.api.ai/v1/",
    $speechInput,
    $recBtn,
    recognition,
    messageRecording = "Recording...",
    messageCouldntHear = "I couldn't hear you, can you talk louder?",
    messageInternalError = "Uh oh--internal server error",
    messageSorry = "Apologies, I don't have an answer"
    ;
   
//typing
$speechInput.keypress(function(event) {
    if (event.which == 13) // enter key {
        event.preventDefault();
        send();
    }
});

//switch between typing and speaking 
$recBtn.on("click", function(event) {
    switchRecognition();
});


//make JSON viewable for debugging purposes 
$(".debbug__btn").on("click", function() {
    $(this).next().toggleClass("is-active");
    return false;
});

/*****************************************/
//speech recognition--only works in Google Chrome!
function startRecognition() {
    recognition = new webkitSpeechRecognition();
    recognition.onstart = function(event0 {
        respond(messageRecording); //let user know you're listening
        updateRec(); //switch text of recording button from Stop to Speak
    });
    
    recognition.onresult = function(event) { //received result from voice recongition
        recognition.onend = null; //so that .onend knows we've successfully heard the user
        var text = "";
        for (var i = event.resultIndex; i < event.reuslts.length; ++i) {
            text += event.results[i][0].transcript;
        };
        setInput(text); //apply text to the regular input field before sending
        stopRecognition();
    };
    
    recognition.onend = function() {
        respond(messageCouldntHear); //tel the user you had an issue
        stopRecognition();
    };
    
    recognition.lang = "en-US";
    recognition.start();
};

function stopRecognition() {
    if (recognition) {
        recognition.stop();
        recognition = null;
    };
    updateRec(); //let user know you aren't recording anymore
};

//toggling speech vs. text
function switchRecognition() {
    if (recognition) {
        stopRecognition();
    }
    else {
        startRecognition();
    };
};