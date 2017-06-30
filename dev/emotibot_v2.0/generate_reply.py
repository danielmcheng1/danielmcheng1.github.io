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
    
    (reflection, emotions) = reflect_emotion(message)
    data["emotions"] = emotions
    
    if BOT_MADE_RANDOM_RESPONSE:
        BOT_MADE_RANDOM_RESPONSE = False
        data["message"] = random.choice(BOT_RANDOM_RESPONSES_AFTER)
    elif random.randint(1, 15) == 1:
        BOT_MADE_RANDOM_RESPONSE = True 
        data["message"] = random.choice(BOT_RANDOM_RESPONSES_BEFORE)
    elif reflection != None:
        data["message"] = reflection
    else: 
        data["message"] = eliza_chatbot.respond(message)
        
    return data
  
def make_initial_greeting():
    data = {"username": BOT_NAME, "message": random.choice(BOT_GREETINGS_OPENING), "emotions": {}}
    return data
    #return "{2}: {0} {1} {2}".format(random.choice(BOT_GREETINGS_OPENING), random.choice(BOT_GREETINGS_NAME), BOT_NAME)


def reflect_emotion(message):
    emotions = get_emotions(message)
    (top, probability) =  get_n_ranked_key(emotions, 1)
    
    if probability > 0.5:
        responses = map_emotions_to_response(emotions)
        return (responses[top], emotions)
    return (None, emotions) 

def map_emotions_to_response(emotions):
    response_mapping = {
        "anger": ["Oh man, you sound [x]", "Uh oh, you seem [x]", "Back off, you [x] person"],
        "fear": ["You seem really [x]", "Don't be [x], I'm here for you"],
        "sadness": ["You sound awfully [x]", "You make me want to cry with your [x] story", "Sigh, that sounds really hard. I'm sorry.", "You sound so [x]. You're really brave for dealing with this"],
        "surprise": ["You seem [x]?", "That must have been a bit unexpected", "You sound [x]. I totally would not have seen that happening myself either"], 
        "joy": ["You sound [x]! That's good to hear.", "You must feel [x]! Let's celebrate (toot-toot)", "That's so awesome, you seem so [x]"]
    }
    
    adjective_mapping = {
        "anger": ["angry", "mad", "choleric"], 
        "fear": ["afraid", "scared"], 
        "joy": ["happy", "glad", "upbeat", "great"], 
        "sadness": ["sad", "unhappy", "gloomy"], 
        "surprise": ["surprised", "shocked"]
    }   
    
    #replace each emotion with one of the above template responses and an adjective synonym for the emotion 
    return {k: random.choice(response_mapping[k]).replace("[x]", random.choice(adjective_mapping[k])) for k, v in emotions.items()}
    
    
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
        