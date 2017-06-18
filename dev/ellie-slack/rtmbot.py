#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True

import glob
import yaml
import json
import os
import sys
import time
import logging

from slackclient import SlackClient

def dbg(debug_string):
    if debug:
        logging.info(debug_string)

class RtmBot(object):
    def __init__(self, token):
        self.token = token
        self.bot_plugins = []
        self.slack_client = None
        self.username = "Ellie"
    def connect(self):
        """Convenience method that creates Server instance"""
        self.slack_client = SlackClient(self.token)
        self.slack_client.rtm_connect()
        
    def start(self):
        self.connect()
        self.load_plugins()
        while True:
            for reply in self.slack_client.rtm_read():
                if "username" in reply:
                    if reply["username"] == self.username:
                        continue
                else:
                    response = self.input(reply)
                    if (response != ""):                    
                        #TBD how does it know what its own username is without a self.username? 
                        #response.response.encode('ascii', 'ignore')
                        #channel.send_message("{}".format(message))
                        #channel = self.slack_client.server.channels.find(output[0])
                       result = self.slack_client.api_call("chat.postMessage", channel = reply["channel"], 
                                                            text = response, username = self.username, icon_emoji=':robot_face:')
            #self.crons()
            #self.output()
            time.sleep(.1)
    def input(self, reply):
        response = ""
        if "type" in reply:
            if reply["type"] == "message":
                data = reply["text"] 
                function_name = "process_" + reply["type"]
                dbg("got {}".format(function_name))
                for plugin in self.bot_plugins:
                    plugin.register_jobs()
                    response = plugin.do(function_name, data)
        return response
    def output(self):
        for plugin in self.bot_plugins:
            limiter = False
            for output in plugin.do_output():
                channel = self.slack_client.server.channels.find(output[0])
                if channel != None and output[1] != None:
                    if limiter == True:
                        time.sleep(1)
                        limiter = False
                    message = output[1].encode('ascii','ignore')
                    channel.send_message("{}".format(message))
                    limiter = True
    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()
    def load_plugins(self):
        #use os.path to ensure compatibility across systems 
        #for plugin in glob.glob(directory+'\plugins\*'):
        plugins_dir = os.path.join(directory, 'plugins', '*')
        for plugin in glob.glob(plugins_dir):
            logging.info(plugin)
            if plugin not in sys.path:
                sys.path.insert(0, plugin)
                #sys.path.insert(0, directory+'\plugins\\')
        #for plugin in glob.glob(directory+'\plugins\*.py') + glob.glob(directory+'\plugins\*/*.py'):
            #name = plugin.split('/')[-1][:-3]
            name = os.path.split(plugin)[1]
        try:
            self.bot_plugins.append(Plugin(name))
        except:
            print ("error loading plugin {0}".format(name))

class Plugin(object):
    def __init__(self, name, plugin_config={}):
        self.name = name
        self.jobs = []
        self.module = __import__(name)
        self.register_jobs()
        self.outputs = []
        if name in config:
            logging.info("config found for: " + name)
            self.module.config = config[name]
        if 'setup' in dir(self.module):
            self.module.setup()
    def register_jobs(self):
        if 'crontable' in dir(self.module):
            for interval, function in self.module.crontable:
                self.jobs.append(Job(interval, eval("self.module."+function)))
            logging.info(self.module.crontable)
            self.module.crontable = []
        else:
            self.module.crontable = []
    def do(self, function_name, data):
        function_name = 'respond'
        if function_name in dir(self.module):
            #this makes the plugin fail with stack trace in debug mode
            if not debug:
                try:
                    return eval("self.module."+function_name)(data)
                except:
                    dbg("problem in module {} {}".format(function_name, data))
            else:
                eval("self.module."+function_name)(data)
        if "catch_all" in dir(self.module):
            try:
                self.module.catch_all(data)
            except:
                dbg("problem in catch all")
    def do_jobs(self):
        for job in self.jobs:
            job.check()
    def do_output(self):
        output = []
        while True:
            if 'outputs' in dir(self.module):
                if len(self.module.outputs) > 0:
                    logging.info("output from {}".format(self.module))
                    output.append(self.module.outputs.pop(0))
                else:
                    break
            else:
                self.module.outputs = []
        return output

class Job(object):
    def __init__(self, interval, function):
        self.function = function
        self.interval = interval
        self.lastrun = 0
    def __str__(self):
        return "{} {} {}".format(self.function, self.interval, self.lastrun)
    def __repr__(self):
        return self.__str__()
    def check(self):
        if self.lastrun + self.interval < time.time():
            if not debug:
                try:
                    self.function()
                except:
                    dbg("problem")
            else:
                self.function()
            self.lastrun = time.time()
            pass

class UnknownChannel(Exception):
    pass


def main_loop():
    if "LOGFILE" in config:
        logging.basicConfig(filename=config["LOGFILE"], level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info(directory)
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        logging.exception('OOPS')

if __name__ == "__main__":
    directory = os.path.dirname(sys.argv[0])
    if not directory.startswith('/'):
        directory = os.path.abspath("{}/{}".format(os.getcwd(),
                                directory
                                ))

    config = yaml.load(open('rtmbot_hidden.conf', 'r')) #Python 3--use open instead of file
    debug = config["DEBUG"]
    bot = RtmBot(os.getenv("SLACK_TOKEN", config["SLACK_TOKEN"]))
    site_plugins = []
    files_currently_downloading = []
    job_hash = {}

    if "DAEMON" in config: #Python 3--use in instead of has_key
        if config["DAEMON"]:
            import daemon
            with daemon.DaemonContext():
                main_loop()
    main_loop()

