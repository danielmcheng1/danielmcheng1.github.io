#built-in modules 
import random 
from nltk.chat.eliza import eliza_chatbot 

#api modules 
import indicoio 
import config_hidden
indicoio.config.api_key = config_hidden.INDICOIO_API_KEY

BOT_NAME = "EmotiBot"

BOT_DEFAULT_RESPONSES = ["I don't understand. Please articulate your thoughts better."]
BOT_GREETINGS_OPENING = ["How're you doing, my friend?", "Hello, good day, and all that jazz. How's it going?", "Greetings and felicitations!"]
BOT_GREETINGS_NAME = ["You can call me", "My name is", "I go by", "My friends call me"]

BOT_RANDOM_RESPONSES_BEFORE = ["Say, do you like eel?", "Do you have a cute puppy?"]
BOT_RANDOM_RESPONSES_AFTER = ["I'm sorry, I got distracted", "Sorry, the world wide web distracted me for a moment"]
BOT_MADE_RANDOM_RESPONSE = False 

def respond_to_message(message):
    global BOT_MADE_RANDOM_RESPONSE 
    data = {"username": BOT_NAME, "message": "", "emotions": {}}
    
    if BOT_MADE_RANDOM_RESPONSE:
        BOT_MADE_RANDOM_RESPONSE = False
        data["message"] = random.choice(BOT_RANDOM_RESPONSES_AFTER)
    elif random.randint(1, 10) == 1:
        BOT_MADE_RANDOM_RESPONSE = True 
        data["message"] = random.choice(BOT_RANDOM_RESPONSES_BEFORE)
    else:
        #(top, emotions) = reflect_emotion(message)
        #if top != None:
        #    return top 
        data["message"] = eliza_chatbot.respond(message)
    return data
  
def make_initial_greeting():
    data = {"username": BOT_NAME, "message": random.choice(BOT_GREETINGS_OPENING), "emotions": {}}
    return data
    #return "{2}: {0} {1} {2}".format(random.choice(BOT_GREETINGS_OPENING), random.choice(BOT_GREETINGS_NAME), BOT_NAME)


def reflect_emotion(message):
    emotions = get_emotions(message)
    adjectives = map_emotions_to_adjectives(emotions)
    (top, probability) =  get_n_ranked_key(adjectives, 1)
    if probability > 0.7:
        return (top, emotions)
    return (None, emotions) 
    
def map_emotions_to_adjectives(emotions):
    mapping = {
        "anger": ["angry", "mad", "upset"], 
        "fear": ["afraid", "scared"], 
        "joy": ["happy", "glad", "upbeat"], 
        "sadness": ["sad", "down", "unhappy", "gloomy"], 
        "surprise": ["surprised", "shocked"]
    }   
    adjectives = {}
    for emotion in emotions:   
        adjective = random.choice(mapping[emotion])
        adjectives[adjective] = emotions[emotion]
    return adjectives
    
def get_n_ranked_key(dict, n):
    if n < 1 or n > len(dict):
        raise ValueError("Invalid trait {n} requested, only {l} keys available".format(n = n, l = len(dict)))
    orderedDict = sorted(dict.items(), key = lambda x: x[1], reverse = True)
    return orderedDict[n - 1]
    
def get_emotions(message):
    '''anger, fear, sadness, surprise, joy'''
    return indicoio.emotion(message)
  
if __name__ == "__main__":
    print(make_initial_greeting())
    while True:
        try:
            user_input = input("Me: ")
            bot_response = respond_to_message(user_input)
            print("{0}: {1}".format(BOT_NAME, bot_response))
        except(KeyboardInterrupt, EOFError, SystemExit):
            break
        