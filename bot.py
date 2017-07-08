import telebot
import token

TOKEN = token()
bot  = telebot.TeleBot(TOKEN.get_token())

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	pass
