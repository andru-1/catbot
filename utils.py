from emoji import emojize # модуль смайликов
from random import choice # выбрать рандомно
import settings
from telegram import ReplyKeyboardMarkup, KeyboardButton # импортируем клавиатуру и кнопки

def get_user_smile(user_data): # что бы не вылетело ошибки и смайл переназначился
	if 'smile' in user_data: # если ключ smile есть, то возвращаем его 
		return user_data['smile']
	else: # если ключа нет, но назначаем новый
		user_data['smile'] = emojize(choice(settings.USER_EMOJI), use_aliases=True) # use_aliases добавляем - потому что у смайлов есть несколько вариантов обозначений
		return user_data['smile']

def get_keyboard():
	contact_button = KeyboardButton('Прислать контакты', request_contact=True)
	location_button = KeyboardButton('Прислать координаты', request_location=True)
	my_keyboard = ReplyKeyboardMarkup([
			['Прислать котика', 'Сменить аватарку'],
			[contact_button, location_button]
		], resize_keyboard=True
	) # делаем кнупку которая вызовет меню кошечек
	return my_keyboard