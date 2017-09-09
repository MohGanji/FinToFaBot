import pymongo
import telebot
from Token import TOKEN
from mongo_auth import dbuser, dbpass


bot = telebot.TeleBot(TOKEN)
db = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1:27017/finToFa' % (dbuser, dbpass)).finToFa

users = db.users.find()

message = raw_input()

for user in users:
    bot.send_message(user.id, message)
