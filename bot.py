# вначале стараться делать выборку из системных библиотек, а потом из сторонних
# стараться делать вывод библиотек по алфавиту
import logging
import locale

from handlers import *

import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler

locale.setlocale(locale.LC_ALL, 'ru')

#print(choice(glob('images/cat*.jp*g')))
#exit()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')

def main():
	mybot = Updater(settings.API_KEY)
	
	logging.info('Бот запускается')
	
	dp = mybot.dispatcher
	# CommandHandler нужно ставить выше MessageHandler - потому что для MessageHandler команда тоже текст
	# pass_user_data=True - сохранение пользовательских данных и во все функции добавим user_data
	dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
	anketa = ConversationHandler(
		entry_points = [RegexHandler('^(Заполнить анкету)$', anketa_start, pass_user_data=True)],
		states = {
			'name': [MessageHandler(Filters.text, anketa_get_name, pass_user_data=True)],
			'rating': [RegexHandler('^(1|2|3|4|5)$', anketa_rating, pass_user_data=True)],
			'comment': [
				MessageHandler(Filters.text, anketa_comment, pass_user_data=True),
				CommandHandler('skip', anketa_skip_comment, pass_user_data=True)
			]
		},
		fallbacks=[MessageHandler(Filters.text, dontknow, pass_user_data=True)]
	)
	dp.add_handler(anketa)
	dp.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True)) # команда /cat
	dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True)) # если приходит текст с "Прислать котика", то вызываем функцию send_cat_picture
	dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True)) # включаем возможность принимать от пользователей фото
	dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True)) # обработка текстовых сообщений
	
	mybot.start_polling()
	mybot.idle()

if __name__ == "__main__": # если файл вызвали на исполнение (напрямую), то выполняй все что находится внутри этого условия, если из файла что-то импортируют, то выполнять условие ненадо 
	main()


