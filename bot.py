import telebot

bot  = telebot.TeleBot("Token")

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	pass
