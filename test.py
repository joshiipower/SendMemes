import telebot
import time
import mysql.connector
import random

################   VARIABLES  ####################

TOKEN = '716938798:AAEDIKSTX68mN-Gmw-3fU8uCXw6unDKb_hk'
GROUP_ID = '-1001283307662'
ADMIN_LIST = [253238481]

COMMANDS_LIST = '/start inicio\n/insertMsg agregar una posible respuesta'

bot = telebot.TeleBot(TOKEN,threaded=False)

def db_start():
	try:
		mydb = mysql.connector.connect(
			host="JoshiiPower.mysql.pythonanywhere-services.com",
			user="JoshiiPower",
			passwd="Xik-wa+PU2",
			database="JoshiiPower$MemesCollective"
		)
		return mydb
	except Exception as e:
	        print str(e)
	        print 'b##########################################'
	        return None


def emojis_list(emoji_number):
	switcher = {
		1:'\xE2\x9D\x8C', 	# tache rojo
		2:'\xF0\x9F\x94\x90', 	# candado
		3:'\xE2\x9C\x85'	# paloma verde
	}
	return switcher.get(emoji_number, "Nothing")

def insert_visit(chat_id):
	try:
		mydb = db_start()
		mycursor = mydb.cursor()
		sql = "INSERT INTO visits (chat_id, visit_date) VALUES (%s, %s)"
		val = (chat_id, time.strftime("%Y-%m-%d %H:%M:%S"))
		mycursor.execute(sql, val)
		mydb.commit()
		mycursor.close()
		mydb.close()
	except Exception as e:
		print str(e)
		print '##########################################'

def validate_user(user_id):
        try:
                mydb = db_start()
                mycursor = mydb.cursor()
		val = (user_id , )
                mycursor.execute("select user_id from first_hi where user_id = %s", val)
                myresult = mycursor.fetchall()

                for row  in myresult:
			mycursor.close()
	                mydb.close()
                        return 1

                mycursor.close()
                mydb.close()
        except Exception as e:
                print str(e)
                print '##########################################'
		return 0

def insert_start(message):
        try:
                mydb = db_start()
                mycursor = mydb.cursor()
                sql = "INSERT INTO first_hi (user_id, first_name, last_name, username) VALUES (%s, %s, %s, %s)"
                val = (message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username)
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.close()
                mydb.close()
        except Exception as e:
                print str(e)
                print '##########################################'

def select():
	try:
		mydb = db_start()
		mycursor = mydb.cursor()
		mycursor.execute("select msg_dsc from msg order by RAND() limit 1")
		myresult = mycursor.fetchall()

		for row  in myresult:
			return row[0]

		mycursor.close()
		mydb.close()
	except Exception as e:
		print str(e)
		print '##########################################'
		__init__()

def insertMsg(message):
	try:
		if message.text.upper() != 'CANCELAR':
			mydb = db_start()
			mycursor = mydb.cursor()
			sql = "INSERT INTO msg (msg_dsc) VALUES (%s)"
			val = (message.text, )
			mycursor.execute(sql, val)
			mydb.commit()
			mycursor.close()
		        mydb.close()
        		bot.send_message(message.chat.id, 'listones')
		else:
			bot.send_message(message.chat.id, 'opearcion cancelada ' + emojis_list(3))
	except Exception as e:
        	print 'caracoles, estoy muriendo x.x (insertMsg())'

#########################################  FUNCIONES HANDLER ######################################


################ INSERTAR MENSAJE #############
# Se asegura que la persona que mando el comando 
# se encuentre en la lista de administradores 

@bot.message_handler(commands=['insertMsg'])
def insert_msg(message):
	if message.chat.id in ADMIN_LIST:
		bot.send_message(message.chat.id, emojis_list(2) + emojis_list(2) +' A R E A   S E G U R A '+emojis_list(2) + emojis_list(2) +
			'\nRecuerda no incluir emojis, ni caracteres especiales como acentos, comas, etc.')
		msg = bot.send_message(message.chat.id, 'Enviame el nuevo mensaje a agregar')
		bot.register_next_step_handler(msg, insertMsg)

################# START #################
# Corre cuando el bot recibe el mensaje 
# /start
# manda un saludo, y almacena la informacion del nuevo usuario
@bot.message_handler(commands=['start'])
def start_handler(message):
#	insert_start(message)
	if validate_user(message.chat.id) is None:
		insert_start(message)
		bot.send_message(message.chat.id, 'qiubo browww send me a memaso')
	else:
		bot.send_message(message.chat.id, 'qiubo ' + message.chat.first_name +' send me a memaso')

################ AIUDAAAA ##############
# Manda una lista de los comandos disponibles
# asi como una breve descripcion del bot 
@bot.message_handler(commands=['help'])
def help_menu(message):
	bot.send_message(message.chat.id, COMMANDS_LIST)

############### PHOTO ###################
# Cuando se le manda una foto al bot
# esta funcion se encarga de descargarla
# renombrarla, guardarla en el servidor y 
# reenviarla al canal de difusion 
@bot.message_handler(content_types=['photo'])
def photo(message):
	fileID = message.photo[-1].file_id
	file_info = bot.get_file(fileID)
	downloaded_file = bot.download_file(file_info.file_path)
	path_f = "Photos/pic" + str(message.chat.id) + "__" + str(message.message_id) + ".jpg"
	with open(path_f, 'wb') as new_file:
        	new_file.write(downloaded_file)
	photo = open (path_f,'rb')
	bot.send_photo(GROUP_ID, photo)
	insert_visit(message.chat.id)

############### Mensaje sensillo ##########
# Cuando recibe un mensaje
# suena esto c: 
@bot.message_handler(func=lambda m: True)
def start_handler(message):
	bot.send_message(message.chat.id, select())

################ MAIN ###################
def __init__():
	try:
        	bot.polling()
	except Exception as e:
	        print str(e)

__init__()

while True:
    time.sleep(100)
