#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import Token
import logging
from subprocess import (PIPE, Popen)


TOKEN = Token.token()
bot  = telebot.TeleBot(TOKEN.get_token())

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi, all you need to do is add me to a group and then reply 'fa or فا' to any message and I will transliterate it for you.\n\
                  or just send me a message"))

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi, all you need to do is add me to a group and then reply 'fa or فا' to any message and I will transliterate it for you.\n\
                  or just send me a message"))

def transliterate(message):
	text = message.reply_to_message.text
    # if((text == "enable" or text == "disable")) and (is_user(message.chat) == True):
    #     return
    user_id = message.from_user.id
    logging.critical(str(user_id)+" : "+text)
    if text:
        if (text[0] == '/'):
            text = text[1:]
        text = text.replace("@TransliterateBot", "")
        text = text.split()
        # user_dictionary = db["user_dicts"].find_one({"user_id": user_id})
        # if(user_dictionary is not None):
        #     text = use_dict(text,user_dictionary["words"])
        # pref = db["user_prefs"].find_one({'user_id': user_id})
        # if(pref is None):
        #     db["user_prefs"].update({'user_id': message.from_user.id}, {'$setOnInsert': {'user_id': message.from_user.id, "denahal": False, "filter": True, "parsi": False}}, upsert = True)
        #     pref = db["user_prefs"].find_one({'user_id': user_id})
        # if(pref["denahal"]):
        #     text = denahalize(text)
        # if(pref["filter"]):
        #     text = filter_text(text)
        # if(pref["parsi"]):
        #     text = parsi_text(text)
        # text = global_replaces(text)
        shcommand = ['php', './behnevis.php']
        shcommand.extend(text)
        p = Popen(shcommand, stdout=PIPE, stderr=PIPE)
        text, err = p.communicate()
        bot.reply_to(message, text)

# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_group_or_user(message):
	if message.chat.type == "private":
		transliterate(message)
	else:
		if message.text == 'fa' or message.text == 'فا':
			transliterate(message.reply_to_message)    

bot.polling()