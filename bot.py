#!/usr/bin/env python
# -*- coding: utf-8 -*-

##### IMPORTS ######
import telebot
import Token
import logging
import flask
import time
import pymongo
from subprocess import (PIPE, Popen)
####################

## CONST MESSAGES ##
START_MESSAGE = "Hi, all you need to do is add me to a group and then reply 'fa or فا' to any message and I will transliterate it for you.\n or just send me a message"

HELP_MESSAGE = "I WILL ADD A HELP MESSAGE SOON"

####################


## INITIALIZATION ##
TOKEN = Token.token()
bot = telebot.TeleBot(TOKEN.get_token())

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

db = pymongo.MongoClient('mongodb://localhost:27017/').finToFa
collections = db.collection_names()
if "users" not in collections:
    db.create_collection("users")
if "words" not in collections:
    db.create_collection("words")


####################


#### FUNCTIONS #####
def transliterate_to_farsi(message):
    """ transliterate finglish messages to farsi, returns farsi text """
    text = message.text
    user_id = message.from_user.id
    logging.critical(str(user_id) + " : " + text)
    if text:
        if text[0] == '/':
            text = text[1:]

        text = text.replace("@TransliterateBot", "")
        text = text.split()
        shcommand = ['php', './behnevis.php']
        shcommand.extend(text)
        pipe = Popen(shcommand, stdout=PIPE, stderr=PIPE)
        text, err = pipe.communicate()
        if err:
            logging.critical("PHP ERR: " + err)
        logging.critical("res : " + str(user_id) + " : " + text)
        return text
####################


##### HANDLERS #####
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """ function for start command """
    new_user = {'id': message.from_user.id, 'username': message.from_user.username}
    if not db.users.find_one({"id" : new_user["id"]}):
        db.users.insert_one()
    bot.reply_to(message,
                 (START_MESSAGE))


@bot.message_handler(commands=['help'])
def help_provider(message):
    """ function for help command """
    bot.reply_to(message,
                 (HELP_MESSAGE))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_group_or_user(message):
    """ check if message is sent to the bot or in a group """
    if message.chat.type == "private":
        text = transliterate_to_farsi(message)
        bot.reply_to(message, text)
    else:
        if message.text == 'fa' or message.text == 'Fa' or message.text == 'فا'.decode('utf-8'):
            msg = message.reply_to_message
            if msg is not None:
                text = transliterate_to_farsi(msg)
                bot.reply_to(msg, text)
            else:
                logging.critical("Err : message is empty")
####################


###### RUNNER ######
bot.polling()
####################
