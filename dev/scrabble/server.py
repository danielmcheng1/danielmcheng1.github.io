
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
    print("Data: {0}".format(str(data)), file = sys.stderr) 
    
    global SCRABBLE_APPRENTICE_DATA 
    #guarantee reset if user refreshes page -- could also check if last_move fille din in the scrabble module?
    if data == {}:
        SCRABBLE_APPRENTICE_DATA = {}
        
    SCRABBLE_APPRENTICE_DATA["scrabble_game_play_wrapper"] = {} 
    SCRABBLE_APPRENTICE_DATA["scrabble_game_play_wrapper"]["last_move"] = data.get("last_move", {})
    
    SCRABBLE_APPRENTICE_DATA = scrabble_apprentice.wrapper_play_next_move(SCRABBLE_APPRENTICE_DATA)
   
    scrabble_game_play_wrapper = SCRABBLE_APPRENTICE_DATA["scrabble_game_play_wrapper"]
    emit('moveDoneComputer', scrabble_game_play_wrapper) 
    
    

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
