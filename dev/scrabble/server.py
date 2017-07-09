
from flask import Flask, render_template, request
import requests

from flask_socketio import SocketIO, emit, send

import scrabble_apprentice 

app = Flask(__name__)
socketio = SocketIO(app)

SCRABBLE_APPRENTICE_RESPONSE = (None, None, None)
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@socketio.on('connect')
def server_originates_message():
    #no client context like when emitting/sending in response to server 
    #hence broadcast=True assumed 
    global SCRABBLE_APPRENTICE_RESPONSE 
    SCRABBLE_APPRENTICE_RESPONSE = scrabble_apprentice.wrapper_make_computer_move(SCRABBLE_APPRENTICE_RESPONSE)
   
    board_obj = SCRABBLE_APPRENTICE_RESPONSE[0]
    socketio.emit('begin play', board_obj)
    
@socketio.on('human play')
def handle_event(data):
    global SCRABBLE_APPRENTICE_RESPONSE 
    SCRABBLE_APPRENTICE_RESPONSE = scrabble_apprentice.wrapper_make_computer_move(SCRABBLE_APPRENTICE_RESPONSE)
   
    board_obj = SCRABBLE_APPRENTICE_RESPONSE[0]
    emit('begin play', board_obj) 
    
    

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
