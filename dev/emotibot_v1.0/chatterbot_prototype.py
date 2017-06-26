from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import os 
import logging



def manual_train():
    logging.basicConfig(level=logging.INFO)
    database_file = 'chatterbot_prototype_database.json'
    
    if os.path.isfile(database_file):
        os.remove(database_file)
        
    bot = ChatBot(
        "Dan",
        storage_adapter = 'chatterbot.storage.JsonFileStorageAdapter',
        input_adapter = 'chatterbot.input.TerminalAdapter',
        trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer',
        output_adapter = 'chatterbot.output.TerminalAdapter',
        database = database_file
        )
        
    bot.train("chatterbot.corpus.english")
    
    bot.set_trainer(ListTrainer)
    bot.train([
        "How're you doing?",
        "I'm good",
        "That is good to hear.",
        "Thank you!",
        "You are weclome.",
        ])
        
    logic_adapters = [
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
        ],
        
if __name__ == "__main__":
    bot_name = "Dan"
    bot = ChatBot(bot_name,
            storage_adapter = "chatterbot.storage.MongoDatabaseAdapter",
            logic_adapters = [
                "chatterbot.logic.BestMatch"
            ],
            filters = [
                "chatterbot.filters.RepetitiveResponseFilter"
            ],
            input_adapter = "chatterbot.input.TerminalAdapter",
            output_adapter = "chatterbot.output.TerminalAdapter",
            database = "chatterbot-database",
            trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer',
    )
        
    bot.train("chatterbot.corpus.english")
    
    print("Hi, my name is {0}".format(bot_name))
    while True:
        try:
            bot_input = bot.get_response(None)
        except(KeyboardInterrupt, EOFError, SystemExit):
            break
        