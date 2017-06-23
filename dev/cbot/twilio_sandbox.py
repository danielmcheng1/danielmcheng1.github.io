from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from flask import Flask, request, redirect
import requests 
import random 
import config_hidden

import generate_reply

TWILIO_ACCOUNT_SID = config_hidden.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = config_hidden.TWILIO_AUTH_TOKEN
TWILIO_FROM_NUMBER = config_hidden.TWILIO_FROM_NUMBER

TWILIO_BASE_URL = "https://{account_sid}:{auth_token}@api.twilio.com/2010-04-01/Accounts/{account_sid}".format(account_sid = TWILIO_ACCOUNT_SID, auth_token = TWILIO_AUTH_TOKEN)

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])        
def respond_to_SMS():    
    messages = requests.get(TWILIO_BASE_URL + "/Messages")
    first_sid = find_first_content("Sid", messages.text)
    
    first_message = requests.get(TWILIO_BASE_URL + "/Messages/" + first_sid)
    first_message_body = strip_trial(find_first_content("Body", first_message.text))
    
    final_response = generate_reply.generateReply(first_message_body)
    resp = MessagingResponse().message(final_response)
    
    return str(resp)
    
    
    '''
    twiml = '<Response><Message>Hello from your Django app!</Message></Response>'
    return HttpResponse(twiml, content_type='text/xml')

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
    '''

def send_message(message, to_number):    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) 
    from_twilio = TWILIO_FROM_NUMBER
    message = client.api.account.messages.create(to=to_number,
                                                 from_=from_twilio,
                                                 body=message)
                                   
                                   
#Utility XML functions 
def find_first_tag(tag, text):
    return text.index(tag)
def find_first_open(tag, text):
    return text.index("<" + tag + ">") + len("<" + tag + ">")
def find_first_close(tag, text):
    return text.index("</" + tag + ">")
def find_first_content(tag, text):
    return text[find_first_open(tag, text) : find_first_close(tag, text)]
def strip_trial(text):
    trial_text = "Sent from your Twilio trial account - "
    if len(text) >= len(trial_text):
        if text[0:len(trial_text)] == trial_text:
            return text[len(trial_text):]
    return text 

    
if __name__ == "__main__":
    app.run(debug=True)
    #send_message("hello again", "+12177227216")
        
    