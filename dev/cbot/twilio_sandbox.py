from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

import random 

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])


def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    #resp = MessagingResponse().message("Hello, Mobile Monkey from Git")
    
    account_sid = "AC50c2f1517cb7744e5a71b56e9bdd013b"
    auth_token = "4a5718f69a6fe0f4da633ecd073674f0"
    client = Client(account_sid, auth_token)    
    all_messages = []
    for sms in client.messages.list():
        message = client.messages(sms.sid).fetch()
        all_messages.append((message.body.encode('utf-8'), message.date_sent))
        #print(message.__dict__)
    all_messages.sort(key = lambda x: x[1], reverse = True)
    #print(*all_messages, sep = '\n')
    resp = all_message[0]
    return str(resp)

def send_message(message, to_number):    
    # Find these values at https://twilio.com/user/account
    account_sid = "AC50c2f1517cb7744e5a71b56e9bdd013b"
    auth_token = "4a5718f69a6fe0f4da633ecd073674f0"
    client = Client(account_sid, auth_token)
    from_twilio = "+12175744267"
    message = client.api.account.messages.create(to=to_number,
                                                 from_=from_twilio,
                                                 body=message)
                                                 
if __name__ == "__main__":
    app.run(debug=True)
    
    #print(*all_messages, sep = '\n')
#why do the field names/attributes not line up at all witih the api?
#good tutorials / links to other resources to set everythign up
        
        
    #send_message("hello again", "+12177227216")