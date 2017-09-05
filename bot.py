#!/usr/bin/env python
# -*- coding: utf-8 -*-

##### IMPORTS ######
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import Token
import logging
import time
from subprocess import (PIPE, Popen)
####################

## CONST MESSAGES ##
START_MESSAGE = "Hi, all you need to do is add me to a group and then reply 'fa or فا' to any message and I will transliterate it for you.\n\
				or just send me a message"


####################


TOKEN = Token.token().get_token()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


##### COMMANDS #####
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=START_MESSAGE)

####################

#### FUNCTIONS #####


def transliterate(message):
    text = message.text
    user_id = message.user.id
    logging.critical(str(user_id) + " : " + text)
    if text:
        if (text[0] == '/'):
            text = text[1:]
        text = text.replace("@TransliterateBot", "")
        text = text.split()
        shcommand = ['php', './behnevis.php']
        shcommand.extend(text)
        p = Popen(shcommand, stdout=PIPE, stderr=PIPE)
        text, err = p.communicate()
        if err:
            logging.critical("PHP ERR: " + err)
        logging.critical("res : " + str(user_id) + " : " + text)
        return text


def finToFa(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=transliterate(update.message))


####################

##### HANDLERS #####
start_handler = CommandHandler('start', startCommand)
dispatcher.add_handler(start_handler)

finToFa_handler = MessageHandler(Filters.text, finToFa)
dispatcher.add_handler(finToFa_handler)
####################

updater.start_webhook(listen='0.0.0.0',
                      port=8443,
                      url_path=TOKEN,
                      webhook_url='https://webhook.mohganji.ir:8443/' + TOKEN)
