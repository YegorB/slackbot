from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re, json
import requests
import logging

logging.basicConfig(format = u'%(asctime)s [%(levelname)-8s] %(message)s', level = logging.DEBUG, filename="slackbot.log")

base_url = "https://base.com/services/tools/bundles"

class EnvBot(object):

    def __init__(self, message):
        self.actions = {
            "status": self.status
        }
        self.message=message

    def status(self, params):
        response = requests.get(base_url, headers={"Content-Type": "application/json"})
        message = ""
        if response.status_code == requests.codes.ok:
            result = response.json()["statuses"]
            if not result:
                self.message.send("No bundles found...")
                return
            for bundle in result:
                if params.lower() in bundle["name"].lower():
                    message += "\n {} >>>> version {} >>>> state {}".format(bundle["name"], bundle["version"], bundle["state"])
        else:
           self.message.send("Maybe environment is down?")
        self.message.send(message)

    def usage(self, job=None, params=None):
        self.message.send("*Usage:*")
        self.message.send("> envbot <action> [<searchString>=<value1>]")
        self.message.send("*Available actions:*")
        v = {}
        for key, value in sorted(self.actions.iteritems()):
            v.setdefault(value, []).append(key)
        for func in v:
            self.message.send("- %s" % ", ".join(v[func]))

    def bad_command(self, cmd):
        self.message.send("Not registered command '%s'. You can specify one from following:" % cmd)
        self.usage()

    def envbot(self, cmd=None):
        args = cmd.split(" ")
        if len(args) < 2:
            self.bad_command(cmd)
            return
        action = args[0]
        params = args[1]
        if action in self.actions:
            self.actions[action](params)
        else:
            self.bad_command(cmd)

@listen_to('envbot (.*)', re.IGNORECASE)
@respond_to('envbot (.*)', re.IGNORECASE)
def envbot(message, cmd=None):
    j = EnvBot(message)
    j.envbot(cmd)


