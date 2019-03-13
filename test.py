import telebot
import time
import mysql.connector
import random

################   VARIABLES

TOKEN = '<TOKEN>'
GROUP_ID = '<CHAT_ID>'
mydb = mysql.connector.connect(
    host="<HOST>",
    user="<USER>",
    passwd="<PASW>",
    database="<DB>"
)

bot = telebot.TeleBot(TOKEN)

def insert(chat_id):
	mycursor = mydb.cursor()
	sql = "INSERT INTO visits (chat_id, visit_date) VALUES (%s, %s)"
	val = (chat_id, time.strftime("%Y-%m-%d %H:%M:%S"))
	mycursor.execute(sql, val)
	mydb.commit()

def select(chat_id):
    mycursor = mydb.cursor()
    mycursor.execute("select msg_dsc from msg order by RAND() limit 1")
	myresult = mycursor.fetchall()
	for row  in myresult:
		return row[0]

@bot.message_handler(commands=['start'])
def start_handler(message):
        bot.send_message(message.chat.id, 'qiubo browww send me a memaso')

#@bot.message_handler(commands=['sendMeAMeme'])
#def start_handler(message):
#	bot.send_message(message.chat.id, 'Okrrrr')
#	photo = open ('Photos/001.jpg','rb')
# bot.send_photo(message.chat.id, photo)
# bot.send_photo(GROUP_ID, photo)

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
