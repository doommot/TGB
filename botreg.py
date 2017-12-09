from datetime import datetime
from account import account
import config
import telebot
from telebot import types

bot = telebot.TeleBot(config.bot_token)
acc=account()

def log(line):
	log_stream = open(config.logfile, "a", encoding = 'utf8')
	mem = 'BREG:' + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S;") + line+'\n'
	log_stream.write(mem)
	log_stream.close()

def save(account_phone):
	log("saving account " + account_phone)
	f=open(config.accountfile,'a')
	f.write(account_phone+'\n')

@bot.message_handler(commands=['start'])
def start(message):
	if message.chat.id in whitelist:
		markup = types.ReplyKeyboardMarkup()
		markup.row('reg')
		bot.send_message(message.chat.id, "BREG ONLINE", reply_markup=markup)
	log("Bot is online by "+str(message.chat.id))

@bot.message_handler(regexp="reg")
def reg(message):
	if message.chat.id in whitelist:
		#acc=account()
		bot.send_message(message.chat.id, "Enter phone:")
@bot.message_handler(regexp="\d\d\d\d\d\d\d\d\d\d\d")
def reg_query(message):
	if message.chat.id in whitelist:
		acc.reg_code_request(message.text)
		bot.send_message(message.chat.id, "Enter code:")
@bot.message_handler(regexp="\d\d\d\d\d")
def code_proceed(message):
	if message.chat.id in whitelist:
		temp_str = acc.reg_auto(message.text)
		log('registration complete '+temp_str)
		acc.subscribe("NeonVision")
		bot.send_message(message.chat.id, "Registered successfuly "+temp_str)

@bot.message_handler(commands=['getlog'])
def getlog(message):
	log("log request from ")
	logfile=open(config.logfile, "r")
	bot.send_message(message.chat.id, logfile.read())

@bot.message_handler(commands=['getstate'])
def getstate(message):
	log("state request from ")
	bot.send_message(message.chat.id, "ONLINE NOW")


whitelist=[116690394, 325581035]#list of chat ids that are allowed to control registration function
if __name__ == '__main__':
	bot.polling(none_stop=True)