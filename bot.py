#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import Token
import logging

TOKEN = Token.token()
bot  = telebot.TeleBot(TOKEN.get_token())

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi there, I am EchoBot.\n"
                  "I am here to echo your kind words back to you."))


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

bot.polling()