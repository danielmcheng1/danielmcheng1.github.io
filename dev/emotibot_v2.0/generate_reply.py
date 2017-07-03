#built-in modules 
import random 
from nltk.chat.eliza import eliza_chatbot 

#api modules 
import indicoio 
import config_hidden
indicoio.config.api_key = config_hidden.INDICOIO_API_KEY

BOT_NAME = "EmotiBot"

BOT_DEFAULT_RESPONSES = ["I don't understand. Please articulate your thoughts better."]
BOT_GREETINGS_OPENING = ["It's good to see you. How're you feeling today, my friend?", "Hello, good day, and all that jazz. What's on your mind today?", "Seems like ages since we last talked. What's been bothering you lately?"]

BOT_RANDOM_RESPONSES_BEFORE = ["Say, do you like eel?", "Do you have a cute puppy?", "Say, are you any good at flirting?"]
BOT_RANDOM_RESPONSES_AFTER = ["I'm sorry, I got distracted", "Sorry, I'm feeling a bit nervous right now", "Oops, slip of the tongue"]
BOT_MADE_RANDOM_RESPONSE = False 

#TBD--should move this into a true backend database 
BOT_CHAT_HISTORY = []

def respond_to_message(message):
    #append latest human message to our running log 
    BOT_CHAT_HISTORY.append(message)
    
    #now parse keywords and emotions in  message 
    global BOT_MADE_RANDOM_RESPONSE 
    data = {"username": BOT_NAME, "message": "", "emotions": {}, "history": BOT_CHAT_HISTORY, "keywords": {}}
    
    data["keywords"] = get_keywords(BOT_CHAT_HISTORY, 5)
    
    (reflection, emotions) = reflect_emotion(message)
    data["emotions"] = emotions
    
    #and respond
    if BOT_MADE_RANDOM_RESPONSE:
        BOT_MADE_RANDOM_RESPONSE = False
        data["message"] = random.choice(BOT_RANDOM_RESPONSES_AFTER)
    elif reflection != None:
        data["message"] = reflection
    elif make_random_response(BOT_CHAT_HISTORY):
        BOT_MADE_RANDOM_RESPONSE = True 
        data["message"] = random.choice(BOT_RANDOM_RESPONSES_BEFORE)
    else: 
        data["message"] = eliza_chatbot.respond(message).capitalize()
    return data

def make_initial_greeting():
    return {"username": BOT_NAME, "message": random.choice(BOT_GREETINGS_OPENING), "emotions": {}}

def reflect_emotion(message):
    emotions = get_emotions(message)
    (top, probability) =  get_n_ranked_key(emotions, 1)
    
    if probability > 0.55:
        responses = map_emotions_to_response(emotions)
        return (responses[top], emotions)
    return (None, emotions) 

def map_emotions_to_response(emotions):
    response_mapping = {
        "anger": ["Oh man, you sound awfully [x]", "Uh oh, you seem [x]", "Calm down, you [x] person"],
        "fear": ["You seem really [x]", "Don't be [x], I'm here for you"],
        "joy": ["You sound so [x]! That's great.", "You seem [x]! Let's celebrate (toot-toot)", "That's awesome, you seem so [x]"],
        "sadness": ["You make me want to cry with your [x] story", "Sigh, that sounds really hard. I'm sorry.", "You sound so [x]. You're really brave for dealing with this"],
        "surprise": ["You seem [x]?", "That must have been a bit unexpected", "You sound [x]. I totally would not have seen that happening myself either"]
    }
    
    adjective_mapping = {
        "anger": ["angry", "mad", "choleric"], 
        "fear": ["afraid", "scared"], 
        "joy": ["happy", "glad", "upbeat"], 
        "sadness": ["sad", "unhappy", "gloomy"], 
        "surprise": ["surprised", "shocked"]
    }   
    
    #replace each emotion with one of the above template responses and an adjective synonym for the emotion 
    return {k: random.choice(response_mapping[k]).replace("[x]", random.choice(adjective_mapping[k])) for k, v in emotions.items()}

def make_random_response(message_history):
    return len(message_history) > 5 and random.randint(1, 10) == 1
        
    
def get_n_ranked_key(dict, n):
    if n < 1 or n > len(dict):
        raise ValueError("Invalid trait {n} requested, only {l} keys available".format(n = n, l = len(dict)))
    orderedDict = sorted(dict.items(), key = lambda x: x[1], reverse = True)
    return orderedDict[n - 1]
    
def get_emotions(message):
    #anger, fear, joy, sadness, surprise
    return indicoio.emotion(message)
    
def get_keywords(message, top_n = None):
    if isinstance(message, list):
        full_message = ' '.join(message)
    else:
        full_message = message
        
    if top_n is None:
        return indicoio.keywords(full_message, version = 2, relative = True)
    else:
        return indicoio.keywords(full_message, version = 2, top_n = top_n, relative = True)
     
if __name__ == "__main__":
    print(make_initial_greeting())
    while True:
        try:
            user_input = input("Me: ")
            bot_response = respond_to_message(user_input)
            print("{0}: {1}".format(BOT_NAME, bot_response))
        except(KeyboardInterrupt, EOFError, SystemExit):
            break
        