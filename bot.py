#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main bot logic
"""

##### IMPORTS ######
import logging
import telebot
from Token import TOKEN
from mongo_auth import dbuser, dbpass
from bot_url import BOT_URL
import pymongo
from utils import *
from init import *
####################


##### HANDLERS #####
@bot.message_handler(commands=['start'])
def initialize(message):
    """ function for start command """
    if not db.users.find_one({'id': message.from_user.id}):
        add_new_user(db, message.from_user.username, message.from_user.id)
    else: logging.info("User exists.")
    txt = str(message.text)
    if len(txt) > len('/start'):
        bot.send_message(message.from_user.id, txt[len('/start'):]+"\nلطفا شکل درست این پیام را به فارسی بنویسید.")
    else:
        bot.reply_to(message,
                     (START_MESSAGE))

@bot.message_handler(commands=['help'])
def help_provider(message):
    """ function for help command """

    bot.reply_to(message,
                 (HELP_MESSAGE))

@bot.message_handler(commands=['contact'])
def contact_creator(message):
    """ function for contact command command """

    bot.reply_to(message,
                 (CONTACT_MESSAGE))

@bot.message_handler(commands=['about'])
def about_me(message):
    """ function for about creator of this bot command """

    bot.reply_to(message,
                 (ABOUT_MESSAGE))


@bot.callback_query_handler(func=lambda callback: True )
def handle_all_callbacks(callback):
    # this runs a function named callback['data'], with callback as the only argument
    globals()[callback.data](callback)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_group_or_user(message):
    """ check if message is sent to the bot or in a group """
    # if not db.users.find_one({'id': message.from_user.id}):
        # add_new_user(db, message.from_user.username, message.from_user.id)
    # else:
    user_reported = db.users.find_one({"id": message.from_user.id})
    if user_reported:
        if user_reported['state'] == REPORT:
            logging.critical("New incoming report:")
            add_report_request(db, message)
            bot.send_message(message.from_user.id, "با تشکر از شما، گزارش شما با موفقیت ثبت شد.")
            accept_message_buttons = [
                {
                    "text": "✅",
                    "data": "accept"
                },
                {
                    "text": "❌",
                    "data": "reject"
                }
            ]
            accept_markup = create_message_markup(accept_message_buttons, row_width=2)
            accept_report_text = "New Report:" + \
                                 "\nFinglish: " + user_reported['report']['finglish_msg'] + \
                                 "\nFarsi: " + user_reported['report']['farsi_msg'] + \
                                 "\nCorrected: " + message.text

            bot.send_message(MY_ID, accept_report_text, reply_markup=accept_markup)
            return
    else:
        logging.critical("ERR: User not found. adding user to database...")
        db.users.insert_one({'id': message.from_user.id, 'username': message.from_user.username,
                             'state': IDLE,
                             'report':{'finglish_msg': "", 'farsi_msg': ""}})

    report_message_buttons = [{
        "text": "اشتباهه؟🗣",
        "data": "wrong"
    }]
    if message.chat.type == "private":
        text = transliterate_to_farsi(message)
        markup = create_message_markup(report_message_buttons)
        bot.reply_to(message, text, reply_markup=markup)
    else:
        if message.text == 'fa' or message.text == 'Fa' or message.text == 'FA' or message.text == 'فا'.decode('utf-8'):
            msg = message.reply_to_message
            if msg is not None:
                text = transliterate_to_farsi(msg)
                markup = create_message_markup(report_message_buttons)
                bot.reply_to(msg, text, reply_markup=markup)
            else:
                logging.critical("Err : message is empty")
####################


## CALLBACK FUNCS ##

def wrong(callback):
    """handle incoming callback for reporting wrong transliterations"""
    if not db.users.find_one({'id': callback.from_user.id}):
        add_new_user(db, callback.from_user.username, callback.from_user.id)
    else: logging.info("In Callback func, User exists.")
    finglish_msg = callback.message.reply_to_message.text
    farsi_msg = callback.message.text
    updated_user = {'id': callback.from_user.id, 'username': callback.from_user.username,
                    'state': REPORT,
                    'report':{'finglish_msg': finglish_msg, 'farsi_msg': farsi_msg}
                   }
    db.users.update({'id': callback.from_user.id}, updated_user)
    logging.info("user reported: " + str(updated_user))
    if callback.message.reply_to_message.chat.type == 'private':
        bot.send_message(callback.from_user.id, str(finglish_msg)+"\nلطفا شکل درست این پیام را به فارسی بنویسید.")
        bot.answer_callback_query(callback.id)
    else:
        bot.answer_callback_query(callback.id, url=BOT_URL+str(finglish_msg))

def accept(callback):
    # add words to database and search from them.
    bot.answer_callback_query(callback.id, text="accepted")

def reject(callback):
    # delete ? record from database
    bot.answer_callback_query(callback.id)

def like(callback):
    pass

####################


###### RUNNER ######
bot.skip_pending = True
bot.polling()
####################
