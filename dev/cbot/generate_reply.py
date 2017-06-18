#built-in modules 
import random 
import traceback 

#own modules 
from sentiment import getSentiment
from linguistic import getPOS 

USER_GREETINGS = ["greetings", "hi", "hello", "hey", "howdy", "whatsup", "sup"]
BOT_GREETINGS = ["Greetings, my friend", "Hello, sir"]

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
        return respondPositive(message)
    elif sentiment >= 0.3:
        return respondNeutral(message)
    else:
        return respondNegative(message)
        
def respondPositive(message):
    bot_positive = ["I'm happy to hear that", "That's awesome, my friend"]
    return random.choice(bot_positive)
    
def respondNeutral(message);
    bot_neutral = ["You seem measured", "You seem neutral"]
    return random.choice(bot_neutral)

def respondNegative(message):
    bot_negative = ["That's too bad", "Go away, you're being negative"]
    return random.choice(bot_negative)
    
'''
Testing 
print(respondToSentiment("I hate you"))
'''