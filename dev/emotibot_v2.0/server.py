
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
def handle_event(data):
    response = generate_reply.respond_to_message(data["message"])
    emit('bot message', response) 
    #send('my send', json=True, callback = acknowledgement()) 
    
@socketio.on('connect')
def server_originates_message():
    #no client context like when emitting/sending in response to server 
    #hence broadcast=True assumed 
    response = generate_reply.make_initial_greeting()
    socketio.emit('begin chat', response)
    
def acknowledgement():
    print("chat received!")
    

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
