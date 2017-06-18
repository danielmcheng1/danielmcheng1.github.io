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
    message_pos = getPOS(message) 
    sentiment = getSentiment(message)
    if len(tokens) > 0 and tokens[0].lower() in USER_GREETINGS:
        return respondToGreeting(message)
    
    youAreJJ = findYouAreJJ(message_pos)
    if (youAreJJ != False):
        if sentiment > 0.5:
            return "Yes, I know I'm " + youAreJJ
        else:
            return "How dare you call me " + youAreJJ
    return respondToSentiment(sentiment, message)
    
def respondToGreeting(message):
    return random.choice(BOT_GREETINGS)
    
def respondToSentiment(sentiment, message):
    if sentiment >= 0.7:
        return respondPositive(message)
    elif sentiment >= 0.3:
        return respondNeutral(message)
    else:
        return respondNegative(message)
        
def respondPositive(message):
    bot_positive = ["I'm happy to hear that", "That's awesome, my friend"]
    return random.choice(bot_positive)
    
def respondNeutral(message):
    bot_neutral = ["You seem measured", "You seem neutral"]
    return random.choice(bot_neutral)

def respondNegative(message):
    bot_negative = ["That's too bad", "Go away, you're being negative"]
    return random.choice(bot_negative)
    
    
def findYouAreJJ(message_pos):
    tokenIndex = 0 
    posIndex = 1
    
    foundYou = False 
    foundYouAre = False 
    for p in message_pos:
        if p[tokenIndex].lower() == "you":
            foundYou = True 
        elif p[tokenIndex].lower() == "are":
            foundYouAre = True 
        if foundYou and foundYouAre and p[posIndex] == "JJ":
             return p[tokenIndex]
    return False 
 
'''
Testing 
print(respondToSentiment("I hate you"))
print(generateReply("You are smart"))
print(generateReply("You are crass"))
'''
