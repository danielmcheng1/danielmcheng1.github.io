from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    resp = MessagingResponse().message("Hello, Mobile Monkey from Git")
    for sms in client.messages.list():
        resp = MessagingResponse().message(sms.to)
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
    #send_message("hello again", "+12177227216")