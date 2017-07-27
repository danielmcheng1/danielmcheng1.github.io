#built-in modules 
import random 
from nltk.chat.eliza import eliza_chatbot
from nltk.chat.rude import rude_chatbot
from nltk.chat.zen import zen_chatbot

#api modules 
import indicoio 
import config_hidden
indicoio.config.api_key = config_hidden.INDICOIO_API_KEY

BOT_DEFAULT_NAME = 'ELIANA'

BOT_GREETINGS_OPENING = {'ELIANA': ["It's good to hear from you. How're you feeling today, my friend?", "Hello, good day, and all that jazz. What's on your mind today?", "Seems like ages since we last talked. What's been bothering you lately?"], \
                         'ANA': ["I sense your presence here in this room. What would you like to discuss today?", "Shall I enlighten you today regarding your past, your present, your future? Your colleagues, your friends, your family?"],
                         'OLGA': ["Well well, look at who is it today, sauntering into my office", "Oh. It's you today, my absolute favorite client"]
BOT_MADE_RANDOM_RESPONSE = {'ELIANA': False, 'ANA': False, 'OLGA': False}
#TBD -- need key for each bot -- move into backend database 
BOT_RANDOM_RESPONSES_BEFORE = ["Say, do you like eel?", "Do you have a cute puppy?", "Say, are you any good at flirting?"]
BOT_RANDOM_RESPONSES_AFTER = ["I'm sorry, I got distracted", "Sorry, I'm feeling a bit nervous right now", "Oops, slip of the tongue"]


#BOT_DEFAULT_RESPONSES = ["I don't understand. Please articulate your thoughts better.", "Sorry, you seem to be having a hard time expressing yourself. Can you try rephrasing?", "What you said doesn't make sense. Can you think a different way to phrase that?"]
#TBD--should move this into a true backend database 
BOT_CHAT_HISTORY = {}

def respond_to_user(user_data):
    message = user_data["message"]
    requested_bot = user_data.get("requested_bot", BOT_DEFAULT_NAME).upper()
    #append latest human message to our running log 
    #append before processing because keyword processing is based on the current message, and not just previous messages 
    BOT_CHAT_HISTORY[requested_bot].append(message)
    
    if len(BOT_CHAT_HISTORY[requested_bot]) == 1:
        return make_initial_greeting(requested_bot)
    else:
        return respond_by_requested_bot(message, requested_bot)
    

def respond_to_message_as_bot(message, requested_bot):
    if requested_bot == 'ELIANA':
        return respond_to_message_as_eliana(message)
    elif requested_bot == 'ANA': #VESTA
        return respond_to_message_as_ana(message)
    elif requested_bot == 'OLGA':
        return respond_to_message_as_olga(message)
    else:
        return respond_to_message_as_unknown(message) 
        
def respond_to_message_as_unknown(message, requested_bot): 
    return {"username": requested_bot, "message": requested_bot + " doesn't exist. And I wouldn't recommend talking to ghosts either"}

def respond_to_message_as_olga(message); 
    this_bot_name = 'OLGA' 
    data = {"username": this_bot_name, "message": "", "history": BOT_CHAT_HISTORY[this_bot_name]}
    data["message"] = rude_chatbot.respond(message) 
    return data 
    
def respond_to_message_as_ana(message):
    this_bot_name = 'ANA'
    data = {"username": this_bot_name, "message": "", "history": BOT_CHAT_HISTORY[this_bot_name]}
    data["message"] = zen_chatbot.respond(message) 
    return data 
    
def respond_to_message_as_eliana(message):
    #now parse keywords in message
    global BOT_MADE_RANDOM_RESPONSE  
    this_bot_name = 'ELIANA'
    data = {"username": this_bot_name, "message": "", "history": BOT_CHAT_HISTORY[this_bot_name], "emotions": {}, "keywords": {}}
    data["keywords"] = get_keywords(BOT_CHAT_HISTORY[this_bot_name], 5)
    
    #parse emotions
    (reflection, emotions) = reflect_emotion(message)
    data["emotions"] = emotions
    
    #and respond
    if BOT_MADE_RANDOM_RESPONSE[this_bot_name]:
        BOT_MADE_RANDOM_RESPONSE[this_bot_name] = False
        data["message"] = random.choice(BOT_RANDOM_RESPONSES_AFTER)

    elif reflection != None:
        #include counter as a safety in case module changes s.t. a user message triggers one deterministic response
        counter = 1
        #reflection is a random response, so keep trying until we get something different 
        while response_matches_previous(reflection, BOT_CHAT_HISTORY[this_bot_name]) and counter < 15:
            (reflection, emotions) = reflect_emotion(message)
            counter = counter + 1
        data["message"] = reflection
    
    elif make_random_response(BOT_CHAT_HISTORY[this_bot_name]):
        BOT_MADE_RANDOM_RESPONSE = True 
        data["message"] = random.choice(BOT_RANDOM_RESPONSES_BEFORE)
    
    else: 
        potential_response = eliza_chatbot.respond(message).capitalize()
        #include counter as a safety in case module changes s.t. a user message triggers one deterministic response
        counter = 1
        #nltk picks a random response, so keep trying until we get something different 
        while response_matches_previous(potential_response, BOT_CHAT_HISTORY[this_bot_name]) and counter < 15:
            potential_response = eliza_chatbot.respond(message).capitalize()
            counter = counter + 1
        data["message"] = potential_response
    return data

def response_matches_previous(response, history):
    if len(history) < 2:
        return False 
    return response.upper() == history[-1].upper() 
    
def make_initial_greeting(requested_bot):
    return {"username": requested_bot, "message": random.choice(BOT_GREETINGS_OPENING)}

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
        "fear": ["You seem really [x]", "Don't be [x], I'm here for you", "You sound a bit [x] about this...?"],
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
        