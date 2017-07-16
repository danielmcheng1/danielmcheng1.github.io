
from flask import Flask, render_template, request
import requests
import sys 

from flask_socketio import SocketIO, emit, send

import scrabble_apprentice 

app = Flask(__name__)
socketio = SocketIO(app)

SCRABBLE_APPRENTICE_DATA = {}
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')


@socketio.on('moveDoneHuman')
def process_human_move(data):
    print("Received human move", file = sys.stderr)
    global SCRABBLE_APPRENTICE_DATA 
    print("Data: {0}".format(str(data)), file = sys.stderr) 
    SCRABBLE_APPRENTICE_DATA["scrabble_game_play_wrapper"] = {} 
    SCRABBLE_APPRENTICE_DATA["scrabble_game_play_wrapper"]["last_move"] = data.get("last_move", {})
    print("Sending over: {0}".format(str(SCRABBLE_APPRENTICE_DATA)), file = sys.stderr) 
    SCRABBLE_APPRENTICE_DATA = scrabble_apprentice.wrapper_play_next_move(SCRABBLE_APPRENTICE_DATA)
   
    scrabble_game_play_wrapper = SCRABBLE_APPRENTICE_DATA["scrabble_game_play_wrapper"]
    emit('moveDoneComputer', scrabble_game_play_wrapper) 
    
    

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
