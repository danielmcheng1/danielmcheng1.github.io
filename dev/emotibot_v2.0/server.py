
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
def server_originates_message():
    #no client context like when emitting/sending in response to server 
    #hence broadcast=True assumed 
    socketio.emit('server originated', {'life': 42})
    
def acknowledgement():
    print("message was received!")
    
def print_form():
    if request.method == 'POST':
        return render_template('form.html',result=request.form['fooput'])
    if request.method == 'GET':
        return render_template('index.html')
'''
export FLASK_APP=server.py
set FLASK_APP=server.py
flask run 
127.0.0.1:5000 or local host
'''

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
