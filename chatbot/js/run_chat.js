//Source: https://www.sitepoint.com/how-to-build-your-own-ai-assistant-using-api-ai/
//Example: https://devdiner.com/demos/barry/

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
    botName = "protoBot";
  
$(document).ready(function() {
    $speechInput = $("#speech");
    $recBtn = $("#rec");
    
    //typing
    $speechInput.keypress(function(event) {
        // enter key 
        if (event.which == 13) {
            event.preventDefault();
            send();
        }
    });

    //switch between typing and speaking 
    $recBtn.on("click", function(event) {
        switchRecognition();
    });


    //make JSON viewable for debugging purposes 
    $(".debug__btn").on("click", function() {
        $(this).next().toggleClass("is-active");
        return false;
    });

    /*****************************************/
    //speech recognition--only works in Google Chrome!
    function startRecognition() {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onstart = function(event) {
            respond(messageRecording); //let user know you're listening
            updateRec(); //switch text of recording button from Stop to Speak
        };
        
        recognition.onresult = function(event) { //received result from voice recongition
            recognition.onend = null; //so that .onend knows we've successfully heard the user
            var text = "";
            console.log(event);
            for (var i = event.resultIndex; i < event.results.length; ++i) {
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

    function setInput(text) {
        $speechInput.val(text);
        send();
    };
    
    function updateRec() {
        $recBtn.text(recognition ? "Stop" : "Speak");
    };

    /***************************************/
    //communicate with Api.Ai
    //standard AJAX POST reuqest using jquery
    //validate we're sending JSON data
    function send() {
        var text = $speechInput.val();
        $.ajax({
            type: "POST",
            url: baseUrl + "query",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            headers: {
                "Authorization": "Bearer " + accessToken
            },
            data: JSON.stringify({query: text, lang: "en", sessionId: "run" + botName}),
            success: function(data) {
                prepareResponse(data); //format the response from API AI
            },
            error: function() {
                respond(messageInternalError);
            }
        });
    };

    function prepareResponse(val) {
        var debugJSON = JSON.stringify(val, undefined, 2);
        var spokenResponse = val.result.speech;
        //TBD what this is for--input or output?
        
        respond(spokenResponse);
        debugRespond(debugJSON);
    };

    function respond(val) {
        //API AI unable to respond -- failed to return a valid response
        if (val == "") {
            val = messageSorry;
        };
        //
        if (val !== messageRecording) { //don't have the page speak that the page is "recording/listening to the user"
            var msg = new SpeechSynthesisUtterance();
            var voices = window.speechSynthesis.getVoices();
            $.each(voices, function(index, value) {
                if (value === "Alex") {
                    msg.voice = value;
                };
            });
            msg.voiceURI = "native";
            msg.text = val;
            msg.lang = "en-US";
            window.speechSynthesis.speak(msg);
        };
        $("#spokenResponse").addClass("is-active").find(".spoken-response__text").html(val);
    };



    //put text into your field for a JSON response
    function debugRespond(val) {
        $("#response").text(val);
    }
});
