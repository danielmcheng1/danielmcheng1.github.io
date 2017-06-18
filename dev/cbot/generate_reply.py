import random 

USER_GREETINGS = ["greetings", "hi", "hello", "hey", "howdy", "whatsup", "sup"]
BOT_GREETINGS = ["Greetings, my friend", "Hello, sir"]

# Generates a bot response from a user message
def generateReply(message):
    tokens = message.split(" ")
    if len(tokens) > 0 and tokens[0].lower() in USER_GREETINGS:
        return respondToGreeting(message)
     
    return "I don't understand." # Otherwise the bot doesn't understand what the user said
    
def respondToGreeting(message):
    return random.choice(BOT_GREETINGS)
