#!/usr/bin/env python
from slackbot.bot import Bot
import logging

logging.basicConfig()

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
