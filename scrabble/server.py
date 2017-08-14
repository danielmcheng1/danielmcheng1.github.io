
from flask import Flask, render_template, request

from flask_socketio import SocketIO, emit, send

import scrabble_apprentice 

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')


@socketio.on('moveDoneHuman')
def process_human_move(data):
    print("Received human move", file = sys.stderr)
    
    #dummy emission to prevent 30 second timeout from server 
    emit('dataReceived', {})
    #guarantee reset if user refreshes page -- could also check if last_move filled in in the scrabble module?
    if data == {}:
        SCRABBLE_APPRENTICE_DATA = {}
    
    #reset the front-end wrapper and save the last move for the back end
    SCRABBLE_APPRENTICE_DATA["scrabble_game_play_wrapper"] = {} 
    SCRABBLE_APPRENTICE_DATA["scrabble_game_play_wrapper"]["last_move"] = data.get("last_move", {})
    #process on the back end
    scrabble_apprentice_data = scrabble_apprentice.wrapper_play_next_move(SCRABBLE_APPRENTICE_DATA)
   
    #return the wrapped play object back to the front end
    scrabble_game_play_wrapper = SCRABBLE_APPRENTICE_DATA["scrabble_game_play_wrapper"]
    emit('moveDoneComputer', scrabble_game_play_wrapper) 
    
    

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
