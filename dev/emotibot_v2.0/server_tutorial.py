'''
LINUX 
export FLASK_APP=server.py

WINDOWS
set FLASK_APP=server.py

flask run 

Go to 127.0.0.1:5000 or localhost:5000

https://flask-socketio.readthedocs.io/en/latest/
'''

from flask import Flask, render_template, request
import requests

from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@socketio.on('my event')
def handle_event(json):
    for key in json:
        print(key, json[key])
    emit('my emit', {"my": 1, "emit": 2}) 
    '''
        socket.on ('my emit', function(data)  { 
            console.log("Emit: Received the following")
            for (var key in data) {
                console.log(key, data[key])
            };
        });
    '''
    send('my send', json=True, callback = acknowledgement()) 
    '''
        socket.on ('message', function(data)  { 
            console.log("Message: Received the following")
            console.log(data)
        });
    '''
@socketio.on('connect')
def server_originates_message():
    #no client context like when emitting/sending in response to server 
    #hence broadcast=True assumed 
    socketio.emit('server originated', {'life': 42})
    '''
    
        socket.on ('server originated', function(data)  { 
            console.log("server originated: Received the following")
            for (var key in data) {
                console.log(key, data[key])
            };
        });
    '''
    
def acknowledgement():
    print("message was received!")
    
def print_form():
    if request.method == 'POST':
        return render_template('form.html',result=request.form['fooput'])
    if request.method == 'GET':
        return render_template('index.html')

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
'''
HTML sample 
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Chat Bot</title>
    <meta charset="utf-8"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>
    <script type="text/javascript" charset="utf-8">
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
    </script>
    <style>
    canvas{
        -moz-user-select: none;
        -webkit-user-select: none;
        -ms-user-select: none;
    }
    </style>
</head>
<body>

</body>

</html>
'''