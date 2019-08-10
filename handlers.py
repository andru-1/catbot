from glob import glob # найти файлы по шаблону (из модуля glob импортируется функция glob)
import logging
from random import choice # выбрать рандомно
from utils import get_keyboard, get_user_smile

 # вывод информации после /start
def greet_user(bot, update, user_data):
	#print('Вызван /start')
	smile = get_user_smile(user_data) # выбрали произвольный смайл с собственной функции
	text_user = 'Привет {}'.format(smile)

	text = 'Вызван /start'
	logging.info(text) # пишем в логи
	update.message.reply_text(text_user, reply_markup=get_keyboard())

def change_avatar(bot, update, user_data):
	if 'smile' in user_data:
		del user_data['smile']
	smile = get_user_smile(user_data)
	update.message.reply_text('Готово: {}'.format(smile), reply_markup=get_keyboard())

def get_contact(bot, update, user_data):
	print(update.message.contact)
	update.message.reply_text('Готово: {}'.format(get_user_smile(user_data)), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
	print(update.message.location)
	update.message.reply_text('Готово: {}'.format(get_user_smile(user_data)), reply_markup=get_keyboard())

def talk_to_me(bot, update, user_data):
	smile = get_user_smile(user_data)
	user_text = "Привет {} {}! Ты написал {}".format(update.message.chat.first_name, smile, update.message.text)
	logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username, update.message.chat.id, update.message.text)
	#user_text = update.message.text #текст который пришел от пользователя
	#print(update.message)
	update.message.reply_text(user_text, reply_markup=get_keyboard())

def send_cat_picture(bot, update, user_data):
	cat_list = glob('images/cat*.jp*g')
	cat_pic = choice(cat_list)

	# send_photo - функция отправки фото
	bot.send_photo(chat_id=update.message.chat_id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())
	# chat_id - выбираем чат, открываем фото (rb - потому что картинка бинарный файл)