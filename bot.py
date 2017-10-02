#!/usr/bin/env python
# -*- coding: utf-8 -*-

##### IMPORTS ######
import logging
import time
import telebot
from Token import TOKEN
from mongo_auth import dbuser, dbpass
from bot_url import BOT_URL
import pymongo
from utils import *
####################

###### STATES ######
IDLE=0
REPORT=1

####################


## CONST MESSAGES ##
START_MESSAGE = "Hi, all you need to do is add me to a group and then reply 'fa or فا' to any message and I will transliterate it for you.\n or just send me a message"
HELP_MESSAGE = "Use this bot to transliterate Finglish messages to Farsi.\n add this bot to your groups, and if you see any finglish message, reply 'fa', 'فا' to the message.\n\nبا این ربات می‌توانید پیام های فینگلیش را به فارسی تبدیل کنید، کافی است ربات را در گروه های خود اضافه کرده و اگر پیام فینگلیش دیدید، در پاسخ به آن بنویسید 'fa' یا 'فا'"
CONTACT_MESSAGE = "please email me :\n mfg1376@gmail.com"
ABOUT_MESSAGE = "من محمد فغان‌پور گنجی هستم،\n اطلاعات بیشتر در مورد من رو در mohganji.ir می‌تونید ببینید"

####################

##### CONSTS #######
MY_ID = 117990761
####################


## INITIALIZATION ##
bot = telebot.TeleBot(TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

db = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1:27017/finToFa' % (dbuser, dbpass)).finToFa

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

def create_message_markup(buttons):
    """ buttons is an array of dictionaries containing text and callback data:
        buttons = [{ 
            "text": "buttonText1", 
            "data": "callBackData1"
        },
        {
            "text": "buttonText2",
            "data": "callBackData2"
        }]
    """
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for button in buttons:
        telebot.types.InlineKeyboardButton(button["text"], callback_data=button["data"])
    buttonReport = telebot.types.InlineKeyboardButton("اشتباهه؟🗣", callback_data="wrong")
    # buttonLike = telebot.types.InlineKeyboardButton("👍", callback_data="correct")
    markup.add(buttonReport)
    return markup

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
                    "text": "accept",
                    "data": "accept"
                },
                {
                    "text": "reject",
                    "data": "reject"
                }
            ]
            accept_markup = create_message_markup(accept_message_buttons)
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
    bot.answer_callback_query(callback.id)

def reject(callback):
    bot.answer_callback_query(callback.id)

def like(callback):
    pass


####################


###### RUNNER ######
bot.skip_pending = True
bot.polling()
####################
