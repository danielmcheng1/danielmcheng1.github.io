#built-in modules 
import random 
import traceback 
import yaml 

#api modules 
import indicoio 
import config_hidden
indicoio.config.api_key = config_hidden.INDICOIO_API_KEY

#own modules 
from sentiment import getSentiment
from linguistic import getPOS 
import ellie 
import nltk_other

USER_GREETINGS = ["greetings", "hi", "hello", "hey", "howdy", "whatsup", "sup"]
BOT_GREETINGS = ["Greetings, my friend", "Hello, sir"]

def getNRankedKey(dict, n):
    if n < 1 or n > len(dict):
        raise ValueError("Invalid trait {n} requested, only {l} keys available".format(n = n, l = len(dict)))
    orderedDict = sorted(dict.items(), key = lambda x: x[1], reverse = True)
    return orderedDict[n - 1]

    
def getPersonalities(message):
    '''extraversion, openness, agreeableness, conscientiousness'''
    #return indicoio.personality(message) 
    '''16 Myers Briggs personality types'''
    return indicoio.personas(message)
    
def getEmotions(message):
    '''anger, fear, sadness, surprise, joy'''
    return indicoio.emotion(message)
    
#-------------------------------------------#    
def cleanTraitAndProbability(tuple):
    return (nounToAdj(tuple[0]), toPercent(tuple[1]))
    
def nounToAdj(token):
    candidates = nltk_other.convertPOS(token, nltk_other.WN_NOUN, nltk_other.WN_ADJECTIVE)
    return " / ".join([c[0] for c in candidates])

def toPercent(num, digits = 0):
    #default floating point representation includes .0 
    if digits == 0:
        return str(round(num * 100)) + "%"
    return str(round(num * 100, digits)) + "%"
    

#-------------------------------------------#
def reflectEmotion(emotions):
    return reflectWrapper(emotions, "You seem", "; or")
    
def reflectPersonality(personalities):
    return reflectWrapper(personalities, "Personality wise, you strike me as", "; or perhaps more like")
    
def reflectWrapper(traits, start, connector):
    response = ""
    for i, v in enumerate(traits.keys()):
        #TBD can make this better 
        (trait, prob) = getNRankedKey(traits, i + 1) 
        if response == "":
            response = "{start} {trait} ({prob})".format(start = start, trait = nounToAdj(trait), prob = toPercent(prob))
        else:
            response = "{prev}{connector} {trait} ({prob})".format(prev = response, connector = connector, trait = nounToAdj(trait), prob = toPercent(prob))    
        break 
    return response 
    

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
    ellieResponse = ellie.respond(message)
    
    #personalities = getPersonalities(message)
    emotions = getEmotions(message) 
    
    reflectedEmotion = reflectEmotion(emotions)
    #reflectedPersonality = reflectPersonality(personalities)
    
    return "[Ellie]: {0} -- [EmotionBot]: {1}".format(ellieResponse, reflectedEmotion) 
    
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
     
def runTests():  
    '''
    print(generateReply("You are smart"))
    print(generateReply("You are crass"))
    print(generateReply("You're smart, I wish I were like you"))
    '''
    print(generateReply("I've been feeling rather down lately. Can you help?"))
runTests()