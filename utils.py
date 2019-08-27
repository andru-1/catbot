import pprint # удобная распечатка словарей
import settings
from clarifai.rest import ClarifaiApp
from telegram import ReplyKeyboardMarkup, KeyboardButton # импортируем клавиатуру и кнопки

def get_keyboard():
	contact_button = KeyboardButton('Прислать контакты', request_contact=True)
	location_button = KeyboardButton('Прислать координаты', request_location=True)
	my_keyboard = ReplyKeyboardMarkup([
			['Прислать котика', 'Сменить аватарку'],
			[contact_button, location_button],
			['Заполнить анкету', 'Показать инлайн клавиатуру']
		], resize_keyboard=True
	) # делаем кнупку которая вызовет меню кошечек
	return my_keyboard


def is_cat(file_name):
	images_has_cat = False # ставим по умолчанию что кота нет
	app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY) # создаем объект с ключем
	model = app.public_models.general_model # берем внутреннюю модель clarifai general_model - с помощью нее делается распознавание
	response = model.predict_by_filename(file_name, max_concepts=5) # предсказать на основе изображения из файла, max_cocepts - макс. количество предсказаний
	#pp = pprint.PrettyPrinter(indent=4) # 4 сколько пробелов для отступа
	#pp.pprint(response)
	if response['status']['code'] == 10000:
		for concept in response['outputs'][0]['data']['concepts']:
			if concept['name'] == 'cat':
				images_has_cat = True # если кот найден
	return images_has_cat # возвращаем статус найденности кота

if __name__ == '__main__':
	print(is_cat('images/cat2.jpg'))