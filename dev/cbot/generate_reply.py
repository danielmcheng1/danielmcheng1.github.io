#built-in modules 
import random 
import traceback 
import yaml 

#api modules 
import indicoio 
f = open('cbot_hidden.conf', 'r')
config = yaml.safe_load(f)
indicoio.config.api_key = config["INDICOIO_API_KEY"]
f.close()


#own modules 
from sentiment import getSentiment
from linguistic import getPOS 
import ellie 

USER_GREETINGS = ["greetings", "hi", "hello", "hey", "howdy", "whatsup", "sup"]
BOT_GREETINGS = ["Greetings, my friend", "Hello, sir"]

def getNRankedKey(dict, n):
    if n < 1 or n > len(dict):
        raise ValueError("Invalid trait {n} requested, only {l} keys available".format(n = n, l = len(dict)))
    orderedDict = sorted(dict.items(), key = lambda x: x[1], reverse = True)
    return orderedDict[n - 1]

    
def getPersonalities(message):
    return indicoio.personality(message) 
    
def getEmotions(message):
    return indicoio.emotion(message)
        
def reflectEmotion(emotions):
    first = getNRankedKey(emotions, 1)
    second = getNRankedKey(emotions, 2)
    response = "You seem {firstEmotion} ({firstProb}), or maybe {secondEmotion} ({secondProb}).".format(
        firstEmotion = first[0], firstProb = toPercent(first[1]), secondEmotion = second[0], secondProb = toPercent(second[1]))
    return response 

def questionPersonality(personalities):
    first = getNRankedKey(personalities, 1)
    last = getNRankedKey(personalities, len(personalities))
    response = "Personality wise, you strike me as {firstPers} ({firstProb}), but have you tried {lastPers} ({lastProb})?".format(
        firstPers = first[0], firstProb = toPercent(first[1]), lastPers = last[0], lastProb = toPercent(last[1]))
    return response 

def toPercent(num, digits = 0):
    #default floating point representation includes .0 
    if digits == 0:
        return str(round(num * 100)) + "%"
    return str(round(num * 100, digits)) + "%"
    

#-------------------------------------------#
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
    
    if len(message_pos) >= 2:
        if (" ".join([x[tokenIndex] for x in message_pos][:2]).lower() == "you are"):
            if message_pos[1][posIndex] == "JJ":
                return message_pos[1][tokenIndex]
    
    if len(message_pos) >= 3:
        if (message_pos[0][tokenIndex].lower() in ["you're", "youre"]):
            if message_pos[2][posIndex] == "JJ":
                return message_pos[2][tokenIndex]
        
    return False 
 
#------------------------------------------------------#

# Generates a bot response from a user message
def generateReply(message):
    tokens = message.split(" ")
    #ellieRespond = getattr(ellie, 'respond') 
    ellieResponse = ellie.respond(message)
    return ellieResponse
    personalities = getPersonalities(message)
    emotions = getEmotions(message) 
    return "{0} {1}".format(reflectEmotion(emotions), questionPersonality(personalities))
    
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
     
  
'''
Testing 
print(respondToSentiment("I hate you"))
print(generateReply("You are smart"))
print(generateReply("You are crass"))

'''
print(generateReply("You're smart, I wish I were like you"))
