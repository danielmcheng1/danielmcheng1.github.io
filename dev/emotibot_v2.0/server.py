
from flask import Flask, render_template, request
import requests
import flask-socketio

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def print_form():
    if request.method == 'POST':
        return render_template('form.html',result=request.form['fooput'])
    if request.method == 'GET':
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
