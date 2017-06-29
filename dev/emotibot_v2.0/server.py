
from flask import Flask, render_template, request
import requests

from flask_socketio import SocketIO, emit, send

BOT_NAME = 'Ellie'
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@socketio.on('human message')
def handle_event(data):
    emit('bot message', {"message": "You said: " + data["message"], 'username': BOT_NAME}) 
    #send('my send', json=True, callback = acknowledgement()) 
    
@socketio.on('connect')
def server_originates_message():
    #no client context like when emitting/sending in response to server 
    #hence broadcast=True assumed 
    socketio.emit('begin chat', {'message': "Hi I'm {0}".format(BOT_NAME), 'username': BOT_NAME})
    
def acknowledgement():
    print("chat received!")
    

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
