#built-in modules 
import random 
import traceback 

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
    return remapEmotions(indicoio.emotion(message))
    
def remapEmotions(emotions):
    mapping = {"anger": "anger", "fear": "fright", "joy": "happiness", "sadness": "sadness", "surprise": "surprised"}   
    remappedEmotions = {}
    for emotion in emotions:
        remappedEmotions[mapping[emotion]] = emotions[emotion]
    return remappedEmotions
    
#-------------------------------------------#    
def cleanTraitAndProbability(tuple):
    return (nounToAdj(tuple[0]), toPercent(tuple[1]))
    
#TBD will rename to adjToSynonyms
def nounToAdj(token, all):
    candidates = nltk_other.convertPOS(token, nltk_other.WN_NOUN, nltk_other.WN_ADJECTIVE)
    if all:
        return " / ".join([c[0] for c in candidates])
    else:
        return random.choice([c[0] for c in candidates]) 
    
def toPercent(num, digits = 0):
    #default floating point representation includes .0 
    if digits == 0:
        return str(round(num * 100)) + "%"
    return str(round(num * 100, digits)) + "%"
    

#-------------------------------------------#
def reflectEmotion(emotions, all):
    if all:
        return reflectAllWrapper(emotions, "You seem", "; or")
    else:
        emotion_to_pattern = {
            "anger": ["Oh man, you sound [x]", "Uh oh, you seem [x]", "Back off, you [x] person"],
            "fright": ["Don't be scared, I'm here for you", "Shoot, you seem really [x]. I'm getting nervous myself", "Ahhhhhhhh scary"],
            "sadness": ["You make me want to cry with your [x] story", "Sigh, that sounds really hard. I'm sorry.", "You sound so [x]. However can you possibly deal?"],
            "surprised": ["Where did *that* come from?", "That must have been a bit unexpected", "What?! I totally would not have seen that happening"], 
            "happiness": ["Hooray, what [x] circumstances!", "You must feel [x]! Let's celebrate (toot-toot)", "That's so awesome, sounds like you're on the path to success"]
        }
 
        (trait, prob) = getNRankedKey(emotions, 1)
        adj_trait = nounToAdj(trait, False)
        
        candidates = emotion_to_pattern[trait]
        pattern = random.choice(candidates)
        choice = pattern.replace("[x]", adj_trait)
        return choice
        
        
def reflectPersonality(personalities, all):
    if all:
        return reflectWrapper(personalities, "Personality wise, you strike me as", "; or perhaps more like")
    else:
        (trait, prob) = getNRankedKey(personalities, 1)
        candidates = [
            "I'd bet your MBTI type is the {0}--but I'm only {1} certain".format(trait, toPercent(prob)),
            "You strike me as the {0} type".format(trait),
            "Now to me, you seem like the {0} type".format(trait),
            "If we were taking a personality test, I'd definitely flag you as the {0}".format(trait)
        ]
        return random.choice(candidates)
        
def reflectAllWrapper(traits, start, connector):
    response = ""
    for i, v in enumerate(traits.keys()):
        #TBD can make this better 
        (trait, prob) = getNRankedKey(traits, i + 1) 
        if response == "":
            response = "{start} {trait} ({prob})".format(start = start, trait = nounToAdj(trait, True), prob = toPercent(prob))
        else:
            response = "{prev}{connector} {trait} ({prob})".format(prev = response, connector = connector, trait = nounToAdj(trait, True), prob = toPercent(prob))    
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
def generateReply(data):
    persona = data.split(" ")[0].upper()
    message = " ".join(data.split(" ")[1:])
    if persona == "ELLIE":
        response = ellie.respond(message)
    elif persona == "EMOTI":
        emotions = getEmotions(message) 
        response = reflectEmotion(emotions, False)
    elif persona == "MBTIMASTER":
        personalities = getPersonalities(message)
        response = reflectPersonality(personalities, False)
    elif persona == "EMOTIALL":
        emotions = getEmotions(message)
        response = reflectEmotion(emotions, True)
    else:
        #default to Ellie 
        response = ellie.respond(message) 
        
    return "{0}".format(response) 
    
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
     
def runTests():  
    print(generateReply("EmotiAll I've been feeling rather down lately. Can you help?"))
    print(generateReply("MBTIMASTER I've been feeling rather down lately. Can you help?"))
#runTests()