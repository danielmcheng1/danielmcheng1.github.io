#built-in modules 
import random 
from nltk.chat.eliza import eliza_chatbot 

#api modules 
import indicoio 
import config_hidden
indicoio.config.api_key = config_hidden.INDICOIO_API_KEY

BOT_DEFAULT_RESPONSES = ["I don't understand. Please articulate your thoughts better."]
BOT_GREETINGS_OPENING = ["How're you doing, my friend?", "Hello, sir/ma'am -- ", "Greetings and felicitations!"]
BOT_GREETINGS_NAME = ["You can call me", "My name is", "I go by", "My friends call me"]
BOT_NAME = "EmotiBot"

def respond_to_message(message):
    return random.choice(BOT_DEFAULT_RESPONSES)

def make_initial_greeting():
    return "{2}: {0} {1} {2}".format(random.choice(BOT_GREETINGS_OPENING), random.choice(BOT_GREETINGS_NAME), BOT_NAME)
    
if __name__ == "__main__":
    print(make_initial_greeting())
    while True:
        try:
            user_input = input("Me: ")
            bot_response = respond_to_message(user_input)
            print("{0}: {1}".format(BOT_NAME, bot_response))
        except(KeyboardInterrupt, EOFError, SystemExit):
            break
        