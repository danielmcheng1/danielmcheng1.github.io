
from flask import Flask, render_template, request, jsonify
#from flask_socketio import SocketIO, emit, send

import sys 
import scrabble_apprentice 

app = Flask(__name__)
#socketio = SocketIO(app)
SCRABBLE_APPRENTICE_DATA = {}

@app.route('/',methods=['GET','POST'])
def play_game():
    return render_template('game.html', data = {'key1': 1, 'key2': 2, 'key3': 4})


@app.route('/moveDoneHuman',methods=['GET','POST'])    
def process_human_move():
    if request.args:
        print('Received args {0}'.format(request.args), file=sys.stderr)
    if request.json:
        print('Received json {0}'.format(request.json), file=sys.stderr)
    
    session_id = 'test' # request.sid
    session_data = SCRABBLE_APPRENTICE_DATA.setdefault(session_id, {})
    
    #reset the front-end wrapper and save the last move for the back end
    session_data["scrabble_game_play_wrapper"] = {} 
    
    #save the last move 
    session_data["scrabble_game_play_wrapper"]["last_move"] = request.json.get("last_move", {})
    
    
    #now process on the back end
    SCRABBLE_APPRENTICE_DATA[session_id] = scrabble_apprentice.wrapper_play_next_move(session_data)
    #print("\After calling scrabble_apprentice module:")
    #print(session_data)
    #return the wrapped play object back to the front end
    scrabble_game_play_wrapper = SCRABBLE_APPRENTICE_DATA[session_id]["scrabble_game_play_wrapper"]
    #emit('moveDoneComputer', scrabble_game_play_wrapper) 
  
    #a = request.args.get('a', 0, type=int)
    #a = request.args.get('keyA')
    #b = request.args.get('keyB') + request.args.get('junk')
    return jsonify(scrabble_game_play_wrapper)
    
#def index():
#    return render_template('index.html')


#@socketio.on('moveDoneHuman')
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
    app.run(host='0.0.0.0', port=5000)
    #socketio.run(app)
