# вначале стараться делать выборку из системных библиотек, а потом из сторонних
# стараться делать вывод библиотек по алфавиту
import logging
import locale

from handlers import *

import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram.ext import messagequeue as mq # очереди

locale.setlocale(locale.LC_ALL, 'ru')

#print(choice(glob('images/cat*.jp*g')))
#exit()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')

# bot - обьекты бота, job - задание
'''
def my_test(bot, job):
	bot.sendMessage(chat_id=157252411, text="Cпам")
	job.interval += 5 # добавление 5 секунд
	if job.interval > 15:
		bot.sendMessage(chat_id=157252411, text="Пока")
		job.schedule_removal() # удаление задачи из очереди
	
	print('Test')
'''

subscribers = set() # хранение и добавление списков

def main():
	mybot = Updater(settings.API_KEY)
	mybot.bot._msg_queue = mq.MessageQueue() # обьявляем переменную _msg_queue как mq.MessageQueue()
	mybot.bot._is_messages_queued_default = True # сообщения по умолчанию должны ставится в очередь

	logging.info('Бот запускается')
	
	dp = mybot.dispatcher

	#mybot.job_queue.run_repeating(my_test, interval=5) # очередь задач с интервалом 5 сек
	mybot.job_queue.run_repeating(send_updates, interval=5)

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
	dp.add_handler(CommandHandler('subscribe', subscribe)) # подписка пользователя
	dp.add_handler(CommandHandler('unsubscribe', unsubscribe)) # отписка пользователя
	dp.add_handler(CommandHandler('alarm', set_alarm, pass_args=True, pass_job_queue=True)) # отправка сообщения пользователю через определенное время, pass_args - текст который пользователь введет после команды бедет разбит по символу пробела и на выходе прийдет список, pass_job_queue - передаем очередь заданий внутрь этой функции
	dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True)) # включаем возможность принимать от пользователей фото
	dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True)) # обработка текстовых сообщений
	
	mybot.start_polling()
	mybot.idle()

if __name__ == "__main__": # если файл вызвали на исполнение (напрямую), то выполняй все что находится внутри этого условия, если из файла что-то импортируют, то выполнять условие ненадо 
	main()


