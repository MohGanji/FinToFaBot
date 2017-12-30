#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
bot initialization
"""

##### IMPORTS ######
import logging
import telebot
from Token import TOKEN
from mongo_auth import dbuser, dbpass
from bot_url import BOT_URL
import pymongo
from utils import *
####################

## INITIALIZATION ##

bot = telebot.TeleBot(TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

db = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1:27017/finToFa' % (dbuser, dbpass)).finToFa

####################
