
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
    send('my send', json=True, callback = acknowledgement()) 
@socketio.on('connect')
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


if __name__ == '__main__':
    #app.run()
    socketio.run(app)
