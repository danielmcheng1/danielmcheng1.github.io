
import sys 
import flask 
#from flask import Flask, render_template, request, jsonify, session
import flask_login 

import scrabble_apprentice 
import server_user_database 

app = flask.Flask(__name__)
app.secret_key = 'temporary secret string'
login_manager = flask_login.LoginManager() 
login_manager.init_app(app)


class User(flask_login.UserMixin): 
    pass 
    
@login_manager.user_loader 
def user_loader(username):
    print('entering user loader with username: ' + str(username))
    if username not in server_user_database.users:
        return 
    user = User() 
    user.id = username 
    return user

@login_manager.request_loader 
def request_loader(request):
    print('entering request loader with request: ' + str(request))
    username = request.form.get('username')
    print('username: ' + username  if username is not None else '')
    if username not in server_user_database.users:
        return 
    user = User()
    user.id = username 
    
    user.is_authenticated = request.form['password'] == users[username]['password']
    return user 

@app.route('/login', methods=['GET', 'POST'])
def login():
    print('entering login function') 
    if flask.request.method == 'GET':
        return flask.render_template('login.html')  
    print('getting data from form')
    username = flask.request.form['username']
    password = flask.request.form['password']
    print('checking')
    if username not in server_user_database.users:
        print('created new user')
        server_user_database.users[username] = {'password': password}
        user = User() 
        user.id = username 
        flask_login.login_user(user) 
        return flask.redirect(flask.url_for('play_game'))
        
    if password == server_user_database.users[username]['password']:
        print('validated!')
        user = User() 
        user.id = username 
        flask_login.login_user(user) 
        return flask.redirect(flask.url_for('play_game'))
        #TBD have to change process_human_move to rerender template 
        #return flask.redirect(flask.url_for('process_human_move'))
   
    print('failed')
    return flask.redirect(flask.url_for('login'), login_failure_message = "Incorrect password. Try again (or create a new username).")

@login_manager.unauthorized_handler 
def unauthorized_handler():
    return flask.redirect(flask.url_for('login'), login_failure_message = "Please sign in (or create a new username).")
        
@app.route('/game',methods=['GET','POST'])
@flask_login.login_required
def play_game():
    print('Logged in as: ' + flask_login.current_user.id)
    return flask.render_template('game.html')


SCRABBLE_APPRENTICE_DATA = {}
@app.route('/moveDoneHuman',methods=['GET','POST'])    
def process_human_move():
    print('Logged in as: ' + flask_login.current_user.id)
    if flask.request.json:
        print('Received json {0}'.format(flask.request.json), file=sys.stderr)
    
    session_id = flask_login.current_user.id
    session_data = SCRABBLE_APPRENTICE_DATA.setdefault(session_id, {})
    user_data = flask.request.json if flask.request.json is not None else {}
    
    #reset the front-end wrapper and save the last move for the back end
    session_data["scrabble_game_play_wrapper"] = {} 
    
    #save the last move 
    session_data["scrabble_game_play_wrapper"]["last_move"] = user_data.get("last_move", {})
    
    
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
    return flask.jsonify(scrabble_game_play_wrapper)
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    #socketio.run(app)
