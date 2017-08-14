
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send

import sys 
import scrabble_apprentice 

app = Flask(__name__)
socketio = SocketIO(app)
SCRABBLE_APPRENTICE_DATA = {}

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')


@socketio.on('moveDoneHuman')
def process_human_move(data):
    #print("Received human move", file = sys.stderr)
    print("Received request {0}, {1}".format(request, request.sid))
    session_id = request.sid
    last_move = data.get("last_move", {})
    
    #dummy emission to prevent 30 second timeout from server 
    emit('dataReceived', {})
    
    #guarantee reset if user refreshes page -- could also check if last_move filled in in the scrabble module?
    if data == {}:
        SCRABBLE_APPRENTICE_DATA[session_id] = {}
    
    #set to {} in case data is somehow missing for this new session ID
    print(SCRABBLE_APPRENTICE_DATA)
    session_data = SCRABBLE_APPRENTICE_DATA.setdefault(session_id, {})
    
    #reset the front-end wrapper and save the last move for the back end
    session_data["scrabble_game_play_wrapper"] = {} 
    
    #save the last move 
    session_data["scrabble_game_play_wrapper"]["last_move"] = last_move 
    
    
    #now process on the back end
    SCRABBLE_APPRENTICE_DATA[session_id] = scrabble_apprentice.wrapper_play_next_move(session_data)
    print("\nresult:")
    print(session_data)
    #return the wrapped play object back to the front end
    scrabble_game_play_wrapper = SCRABBLE_APPRENTICE_DATA[session_id]["scrabble_game_play_wrapper"]
    emit('moveDoneComputer', scrabble_game_play_wrapper) 
    
    

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
