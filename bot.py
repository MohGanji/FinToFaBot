#!/usr/bin/env python
# -*- coding: utf-8 -*-

##### IMPORTS ######
import telebot
import Token
import logging
import flask
import time
from subprocess import (PIPE, Popen)
####################

## CONST MESSAGES ##
START_MESSAGE = "Hi, all you need to do is add me to a group and\
             then reply 'fa or فا' to any message and I will transliterate it for you.\n\
				or just send me a message"

HELP_MESSAGE = "I WILL ADD A HELP MESSAGE SOON"

####################

TOKEN = Token.token()
bot = telebot.TeleBot(TOKEN.get_token())

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# Handle '/start' and '/help'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """ function for start command """
    bot.reply_to(message,
                 (START_MESSAGE))


@bot.message_handler(commands=['help'])
def help_provider(message):
    """ function for help command """
    bot.reply_to(message,
                 (HELP_MESSAGE))


def transliterate_to_farsi(message):
    """ transliterate finglish messages to farsi """
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
        logging.critical("PHP ERR: " + err)
        logging.critical("res : " + str(user_id) + " : " + text)
        return text

# Handle all other messages


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_group_or_user(message):
    """ check if message is sent to the bot or in a group """
    if message.chat.type == "private":
        transliterate_to_farsi(message)
    else:
        if message.text == 'fa' or message.text == 'Fa' or message.text == 'فا'.decode('utf-8'):
            msg = message.reply_to_message
            if msg is not None:
                text = transliterate_to_farsi(msg)
                bot.reply_to(msg, text)
            else:
                logging.critical("Err : message is empty")


bot.polling()
