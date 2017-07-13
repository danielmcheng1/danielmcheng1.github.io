
from flask import Flask, render_template, request
import requests

from flask_socketio import SocketIO, emit, send

import scrabble_apprentice 

app = Flask(__name__)
socketio = SocketIO(app)

SCRABBLE_APPRENTICE_DATA = {}
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@socketio.on('startGame')
def start_game():
    global SCRABBLE_APPRENTICE_DATA
    SCRABBLE_APPRENTICE_DATA = scrabble_apprentice.wrapper_play_next_move(SCRABBLE_APPRENTICE_DATA)
    scrabble_game_play_wrapper = SCRABBLE_APPRENTICE_DATA["scrabble_game_play_wrapper"]
    socketio.emit('moveDoneComputer',scrabble_game_play_wrapper)
    
@socketio.on('moveDoneHuman')
def process_human_move(data):
    global SCRABBLE_APPRENTICE_DATA 
    SCRABBLE_APPRENTICE_DATA["placed_tiles_human"] = data.get("placedTilesHuman", {})
    SCRABBLE_APPRENTICE_DATA = scrabble_apprentice.wrapper_play_next_move(SCRABBLE_APPRENTICE_DATA)
   
    scrabble_game_play_wrapper = SCRABBLE_APPRENTICE_DATA["scrabble_game_play_wrapper"]
    emit('moveDoneComputer', scrabble_game_play_wrapper) 
    
    

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
