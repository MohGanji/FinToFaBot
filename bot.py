import telebot
import token

TOKEN = token.token()
bot  = telebot.TeleBot(TOKEN.get_token())

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	bot.reply_to(message, "hellow")

bot.set_webhook(url="https://vmoh.ir/mohammad/toFarsiBot/bot.py")

#bot.polling()
