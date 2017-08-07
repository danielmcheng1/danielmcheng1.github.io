
from flask import Flask, render_template, request
import requests
import generate_reply 

from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@socketio.on('human message')
def handle_human_message(data):
    response = generate_reply.respond_to_user(data)
    emit('bot message', response) 

@socketio.on('begin chat')
def handle_begin_chat(requested_bot):
    response = generate_reply.make_initial_greeting(requested_bot) 
    emit('bot message', response)
    
if __name__ == '__main__':
    #app.run()
    socketio.run(app)
