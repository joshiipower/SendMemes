import telebot
import time
import mysql.connector
import random

################   VARIABLES

TOKEN = ''
GROUP_ID = ''
ADMIN_LIST = []

COMMANDS_LIST = '/start inicio\n/insertMsg agregar una posible respuesta'

mydb = mysql.connector.connect(
    host="",
    user="",
    passwd="",
    database=""
)

bot = telebot.TeleBot(TOKEN)

def emojis_list(emoji_number):
	switcher = {
		1:'\xE2\x9D\x8C', 	# tache rojo
		2:'\xF0\x9F\x94\x90', 	# candado
		3:'\xE2\x9C\x85'	# paloma verde
	}
	return switcher.get(emoji_number, "Nothing")

def insert(chat_id):
	try:
		mycursor = mydb.cursor()
		sql = "INSERT INTO visits (chat_id, visit_date) VALUES (%s, %s)"
		val = (chat_id, time.strftime("%Y-%m-%d %H:%M:%S"))
		mycursor.execute(sql, val)
		mydb.commit()
	except Exception as e:
                bot.reply_to(msg, 'caracoles, estoy muriendo x.x')

def select(chat_id):
	try:
		mycursor = mydb.cursor()
		mycursor.execute("select msg_dsc from msg order by RAND() limit 1")
		myresult = mycursor.fetchall()

		for row  in myresult:
			return row[0]
	except Exception as e:
                bot.reply_to(msg, 'caracoles, estoy muriendo x.x')

def insertMsg(message):
	try:
		if message.text.upper() != 'CANCELAR':
			mycursor = mydb.cursor()
        	        sql = "INSERT INTO msg (msg_dsc) VALUES (%s)"
			val = (message.text ,)
	                mycursor.execute(sql, val)
        	        mydb.commit()
                	bot.send_message(message.chat.id, 'listones')
		else:
			bot.send_message(message.chat.id, 'opearcion cancelada ' + emojis_list(3))
	except Exception as e:
        	bot.reply_to(message, 'oooops :c')

@bot.message_handler(commands=['insertMsg'])
def insert_msg(message):
	if message.chat.id in ADMIN_LIST:
		bot.send_message(message.chat.id, emojis_list(2) + emojis_list(2) +' A R E A   S E G U R A '+emojis_list(2) + emojis_list(2))
		msg = bot.send_message(message.chat.id, 'Enviame el nuevo mensaje a agregar')
		bot.register_next_step_handler(msg, insertMsg)
	else:
		bot.send_message(message.chat.id, emojis_list(1) +'  A C C E S O   D E N E G A D O  ' + emojis_list(1))

@bot.message_handler(commands=['start'])
def start_handler(message):
        bot.send_message(message.chat.id, 'qiubo browww send me a memaso')

@bot.message_handler(commands=['help'])
def help_menu(message):
	bot.send_message(message.chat.id, COMMANDS_LIST)

#@bot.message_handler(commands=['sendMeAMeme'])
#def start_handler(message):
#	bot.send_message(message.chat.id, 'Okrrrr')
#	photo = open ('Photos/001.jpg','rb')
	#bot.send_photo(message.chat.id, photo)
	#bot.send_photo(-1001283307662, photo)

@bot.message_handler(content_types=['photo'])
def photo(message):
	fileID = message.photo[-1].file_id
	file_info = bot.get_file(fileID)
	downloaded_file = bot.download_file(file_info.file_path)
	path_f = "Photos/pic" + str(message.chat.id) + "__" + str(message.message_id) + ".jpg"
	with open(path_f, 'wb') as new_file:
        	new_file.write(downloaded_file)
	bot.send_message(message.chat.id, 'okrrrr')
	photo = open (path_f,'rb')
	bot.send_photo(GROUP_ID, photo)
	insert(message.chat.id)

@bot.message_handler(func=lambda m: True)
def start_handler(message):
	bot.send_message(message.chat.id, select(message.chat.id))

bot.polling()
