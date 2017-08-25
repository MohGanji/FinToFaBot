#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import Token
import logging
import flask
import time
from subprocess import (PIPE, Popen)


TOKEN = Token.token()
bot  = telebot.TeleBot(TOKEN.get_token())

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

#########
# webhook preparation

WEBHOOK_HOST = 'mohganji.ir'
WEBHOOK_PORT = '8443'
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = "/etc/letsencrypt/live/mohganji.ir/cert.pem"
WEBHOOK_PRIV_CERT = "/etc/letsencrypt/live/mohganji.ir/privkey.pem"

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN.get_token())

router = flask.Flask(__name__)

@router.route('/', methods=['GET', 'HEAD'])
def index():
	return 'OK'

@router.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
	print "well here is an answer"
	if flask.request.headers.get('content-type') == 'application/json':
		json_string = flask.request.json
		print json_string
		print json_string["message"]["text"]
		#update = bot.types.Update.de_json(json_string)
		#bot.process_new_updates([update])
		return ''
	else:
		print "aborting!!:" + flask.request.headers.headers.get('content-type')
		flask.abort(403)



##########

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

def transliterate_to_farsi(message):
	text = message.text
	user_id = message.from_user.id
	logging.critical(str(user_id)+" : "+text)
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
			logging.critical("PHP ERR: "+ err)
		logging.critical("res : "+str(user_id)+" : "+text)
		bot.reply_to(message, text)

# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_group_or_user(message):
	if message.chat.type == "private":
		transliterate_to_farsi(message)
	else:
		if message.text == 'fa' or message.text == 'Fa' or message.text == 'فا'.decode('utf-8'):
			msg = message.reply_to_message
			if msg is not None:
				transliterate_to_farsi(msg)
			else:
				logging.critical("Err : message is empty")

bot.remove_webhook()
time.sleep(3)

#bot.polling()


bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))
print WEBHOOK_URL_BASE+WEBHOOK_URL_PATH
router.run(host=WEBHOOK_LISTEN, port=int(WEBHOOK_PORT), ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_PRIV_CERT), debug=True)
