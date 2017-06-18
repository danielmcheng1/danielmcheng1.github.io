#built-in modules 
import random 
import traceback 

#own modules 
from sentiment import getSentiment

USER_GREETINGS = ["greetings", "hi", "hello", "hey", "howdy", "whatsup", "sup"]
BOT_GREETINGS = ["Greetings, my friend", "Hello, sir"]
BOT_POSITIVE = ["I'm happy to hear that", "That's awesome, my friend"]
BOT_NEGATIVE = ["That sucks", "That's too bad"]
BOT_NEUTRAL = ["You seem measured"]

# Generates a bot response from a user message
def generateReply(message):
    tokens = message.split(" ")
    if len(tokens) > 0 and tokens[0].lower() in USER_GREETINGS:
        return respondToGreeting(message)
    
    return respondToSentiment(message)
    # Otherwise the bot doesn't understand what the user said
    #return "I don't understand." 
    
def respondToGreeting(message):
    return random.choice(BOT_GREETINGS)
    
def respondToSentiment(message):
    sentiment = getSentiment(message)

    if sentiment >= 0.7:
        return random.choice(BOT_POSITIVE)
    elif sentiment >= 0.3:
        return random.choice(BOT_NEUTRAL)
    else:
        return random.choice(BOT_NEGATIVE)
'''
Testing 
print(respondToSentiment("I hate you"))
'''