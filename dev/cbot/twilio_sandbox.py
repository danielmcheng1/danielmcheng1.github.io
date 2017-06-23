from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

import random 
import config_hidden

TWILIO_ACCOUNT_SID = config_hidden.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = config_hidden.TWILIO_AUTH_TOKEN
TWILIO_FROM_NUMBER = config_hidden.TWILIO_FROM_NUMBER

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])



def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    #resp = MessagingResponse().message("Hello, Mobile Monkey from Git")
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)    
    all_messages = []
    for sms in client.messages.list():
        message = client.messages(sms.sid).fetch()
        all_messages.append((message.body.encode('utf-8'), message.date_sent))
        #print(message.__dict__)
    all_messages.sort(key = lambda x: x[1], reverse = True)
    #print(*all_messages, sep = '\n')
    resp = all_messages[0]
    return str(resp)

def send_message(message, to_number):    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) 
    from_twilio = TWILIO_FROM_NUMBER
    message = client.api.account.messages.create(to=to_number,
                                                 from_=from_twilio,
                                                 body=message)
                                                 
if __name__ == "__main__":
    app.run(debug=True)
    
    #send_message("hello again", "+12177227216")
    
    #why do the field names/attributes not line up at all witih the api?
    #good tutorials / links to other resources to set everythign up
        
        
    