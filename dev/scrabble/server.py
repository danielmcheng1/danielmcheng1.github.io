
from flask import Flask, render_template, request
import requests

from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@socketio.on('human play')
def handle_event(data):
    emit('bot play', response) 
    
@socketio.on('connect')
def server_originates_message():
    #no client context like when emitting/sending in response to server 
    #hence broadcast=True assumed 
    socketio.emit('begin play', response)
    
    

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
