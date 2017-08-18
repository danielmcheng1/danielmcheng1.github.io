
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
    print('entering user loader')
    if username not in server_user_database.users:
        return 
    user = User() 
    user.id = username 
    return user

@login_manager.request_loader 
def request_loader(request):
    print('entering request loader')
    username = request.form.get('username')
    if username not in server_user_database.users:
        return 
    user = User()
    user.id = email 
    
    user.is_authenticated = request.form['pw'] == users[username]['pw']
    return user 
    
SCRABBLE_APPRENTICE_DATA = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
            <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
            </form>
            '''    
    username = flask.request.form['username']
    pw = flask.request.form['pw']
    print('checking')
    if username not in server_user_database.users:
        print('created new user')
        server_user_database.users[username] = {'pw': pw}
    if pw == server_user_database.users[username]['pw']:
        print('validated!')
        user = User() 
        user.id = username 
        print('logging in')
        flask_login.login_user(user) 
        print('redirectig')
        return flask.redirect(flask.url_for('play_game'))
    else:
        print('failed')
        return flask.redirect(flask.url_for('login'))

@login_manager.unauthorized_handler 
def unauthorized_handler():
    return 'Unauthorized. Please sign in'
        
@app.route('/protected',methods=['GET','POST'])
@flask_login.login_required
def play_game():
    print('Logged in as: ' + flask_login.current_user.id)
    return flask.render_template('game.html', data = {'key1': 1, 'key2': 2, 'key3': 4})


@app.route('/moveDoneHuman',methods=['GET','POST'])    
def process_human_move():
    print('Logged in as: ' + flask_login.current_user.id)
    if flask.request.args:
        print('Received args {0}'.format(flask.request.args), file=sys.stderr)
    if flask.request.json:
        print('Received json {0}'.format(flask.request.json), file=sys.stderr)
    
    session_id = 'test' # request.sid
    session_data = SCRABBLE_APPRENTICE_DATA.setdefault(session_id, {})
    
    #reset the front-end wrapper and save the last move for the back end
    session_data["scrabble_game_play_wrapper"] = {} 
    
    #save the last move 
    session_data["scrabble_game_play_wrapper"]["last_move"] = flask.request.json.get("last_move", {})
    
    
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
