
from flask import Flask, render_template, request
import requests

from flask_socketio import SocketIO, emit, send

import scrabble_apprentice 

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@socketio.on('connect')
def server_originates_message():
    #no client context like when emitting/sending in response to server 
    #hence broadcast=True assumed 
    response = scrabble_apprentice.wrapper_make_computer_move()
    socketio.emit('begin play', str(response))
    
@socketio.on('human play')
def handle_event(data):
    response = scrabble_apprentice.wrapper_make_computer_move
    emit('bot play', response) 
    
    

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
