from glob import glob # найти файлы по шаблону (из модуля glob импортируется функция glob)
import logging
import os # функции операционной системы (создание файлов, папок...)
from random import choice # выбрать рандомно

from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode # убирает клавиатуру, показыве клавиатуру, возможность форматирования (html или markdovn)
from telegram.ext import ConversationHandler # завершение диалога
from telegram.ext import messagequeue as mq # очереди

from utils import get_keyboard, is_cat

from bot import subscribers # вызвали список подписчиков

from db import db, get_or_create_user, get_user_smile

 # вывод информации после /start
def greet_user(bot, update, user_data):
	#print(update.effective_user) # данные от пользователя
	#print(update.message)
	#print(update.message.chat_id)
	#print('Вызван /start')
	user = get_or_create_user(db, update.effective_user, update.message)
	smile = get_user_smile(db, user) # выбрали произвольный смайл с собственной функции
	user_data['smile'] = smile
	text_user = 'Привет {}'.format(smile)

	text = 'Вызван /start'
	logging.info(text) # пишем в логи
	update.message.reply_text(text_user, reply_markup=get_keyboard())

def change_avatar(bot, update, user_data):
	user = get_or_create_user(db, update.effective_user, update.message)
	if 'smile' in user:
		del user['smile']
	smile = get_user_smile(db, user)
	update.message.reply_text('Готово: {}'.format(smile), reply_markup=get_keyboard())

def get_contact(bot, update, user_data):
	user = get_or_create_user(db, update.effective_user, update.message)
	#print(update.message.contact)
	update.message.reply_text('Готово: {}'.format(get_user_smile(db, user)), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
	user = get_or_create_user(db, update.effective_user, update.message)
	print(update.message.location)
	update.message.reply_text('Готово: {}'.format(get_user_smile(db, user)), reply_markup=get_keyboard())

def talk_to_me(bot, update, user_data):
	user = get_or_create_user(db, update.effective_user, update.message)
	smile = get_user_smile(db, user)
	user_text = "Привет {} {}! Ты написал {}".format(user['first_name'], smile, update.message.text)
	logging.info("User: %s, Chat id: %s, Message: %s", user['username'].username, update.message.chat.id, update.message.text)
	#user_text = update.message.text #текст который пришел от пользователя
	#print(update.message)
	update.message.reply_text(user_text, reply_markup=get_keyboard())

def send_cat_picture(bot, update, user_data):
	user = get_or_create_user(db, update.effective_user, update.message)
	cat_list = glob('images/cat*.jp*g')
	cat_pic = choice(cat_list)

	# send_photo - функция отправки фото
	bot.send_photo(chat_id=update.message.chat_id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())
	# chat_id - выбираем чат, открываем фото (rb - потому что картинка бинарный файл)

def check_user_photo(bot, update, user_data):
	user = get_or_create_user(db, update.effective_user, update.message)
	update.message.reply_text('Обрабатываю фото')
	os.makedirs('downloads', exist_ok=True) # создаем папку и не выбрасывае исключение даже если ее не существует
	photo_file = bot.getFile(update.message.photo[-1].file_id) # если в бот присылается файл, то телеграмм сам его конвертирует в jpg и созадет несколько вариантов файла (превью), update.message.photo[-1] берем последний элемент (оригинальное изображение), file_id - идентификатор файла
	filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id)) # os.path.join - соединяем название файлов и папок между собой по правильным слешам, пусть сохранение файла и название - это id - это путь до файла
	photo_file.download(filename) # скачиваем файл
	update.message.reply_text('Файл сохранен')
	if is_cat(filename):
		update.message.reply_text('Котик обнаружен, добавлено в библиотеку')
		new_filename = os.path.join('images', 'cat_{}.jpg'.format(photo_file.file_id))
		os.rename(filename, new_filename) # перемещаем файл и переименовываем его
	else:
		update.message.reply_text('Котик не обнаружен, не добавлено в библиотеку')
		os.remove(filename) # удаляем файл если там нету котика

def anketa_start(bot, update, user_data):
	user = get_or_create_user(db, update.effective_user, update.message)
	update.message.reply_text('Как вас зовут? Напишите имя и фамилию', reply_markup=ReplyKeyboardRemove())
	return 'name' # возвращает чекпоинт следующего шага

def anketa_get_name(bot, update, user_data):
	user = get_or_create_user(db, update.effective_user, update.message)
	user_mame = update.message.text # получили текст от пользователя
	# проверим что есть 2 слова
	if len(user_mame.split(' ')) != 2:
		update.message.reply_text('Пожалуйста, введите имя и фамилию')
		return 'name' # и возвращаем на предидущий чекпоинт
	else:
		user_data['anketa_name'] = user_mame # сохраняем его имя
		reply_keyboard = [['1', '2', '3', '4', '5']]
		update.message.reply_text(
			'Оцените бота от 1 до 5',
			reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True) # one_time_keyboard - после клика клавиатура автоматом скрывается
		)
		return 'rating'

def anketa_rating(bot, update, user_data):
	user = get_or_create_user(db, update.effective_user, update.message)
	user_data['anketa_rating'] = update.message.text
	# ''' многострочная строка
	update.message.reply_text('''Пожалуйста напишите отзыв или нажмите /skip для выхода''')
	return 'comment'

def anketa_comment(bot, update, user_data):
	user = get_or_create_user(db, update.effective_user, update.message)
	user_data['anketa_comment'] = update.message.text
	text = """
<b>Фамилия Имя:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}
<b>Комментарий:</b> {anketa_comment}
	""".format(**user_data) # при подстановке format сам определит ключи из user_data
	update.message.reply_text(text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
	return ConversationHandler.END

def anketa_skip_comment(bot, update, user_data):
	user = get_or_create_user(db, update.effective_user, update.message)
	text = """
<b>Фамилия Имя:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}
	""".format(**user_data) # при подстановке format сам определит ключи из user_data
	update.message.reply_text(text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
	return ConversationHandler.END

def dontknow(bot, update, user_data):
	user = get_or_create_user(db, update.effective_user, update.message)
	update.message.reply_text('Не понимаю')

def subscribe(bot, update):
	user = get_or_create_user(db, update.effective_user, update.message)
	subscribers.add(update.message.chat_id)
	update.message.reply_text('Вы подписались')
	print(subscribers)

def unsubscribe(bot, update):
	user = get_or_create_user(db, update.effective_user, update.message)
	if update.message.chat_id in subscribers: # проверка на то подписан ли пользователь
		subscribers.remove(update.message.chat_id)
		update.message.reply_text('Вы отписались')
	else: # если такого чата нету
		update.message.reply_text('Вы не подписаны, нажмите /subscribe для подписки')

# декоратор - функция, которая оборачивает в себя нижестоящую функцию, send_updates передается mq.queuedmessage для очереди
@mq.queuedmessage
def send_updates(bot, job):
	for chat_id in subscribers: # в цикле перебираем подписчиков
		bot.sendMessage(chat_id=chat_id, text='текст')

def set_alarm(bot, update, args, job_queue): # bot - данные бота, args - список пришедших аргументов переданных телеграмом, job_queue - рычаг для очереди задач
	user = get_or_create_user(db, update.effective_user, update.message)
	try:
		seconds = abs(int(args[0])) # берем нулевой элемент, переводим в число и абсолютное значение
		job_queue.run_once(alarm, seconds, context=update.message.chat_id) # выполнить 1, alarm - функция которой передается задача c переменными, seconds - через сколько секунд надо выполнить, context = id пользователя которому надо передать
	except (IndexError, ValueError):
		update.message.reply_text('введите число секунд после /alarm')

@mq.queuedmessage
def alarm(bot, job):
	bot.send_message(chat_id=job.context, text='Сработал будильник')