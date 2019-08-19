from pymongo import MongoClient
import settings
from emoji import emojize # модуль смайликов
from random import choice # выбрать рандомно

db = MongoClient(settings.MONGO_LINK)[settings.MONGO_DB]

# находим пользователя или сохраняем его в базу
def get_or_create_user(db, effective_user, message):
	user = db.users.find_one({'user_id': effective_user.id}) # запрос, users - название ключа
	print(user)

	if not user:
		user = {
			'user_id': effective_user.id,
			'first_name': effective_user.first_name,
			'last_name': effective_user.last_name,
			'username': effective_user.username,
			'chat_id': message.chat.id
		}
		db.users.insert_one(user)

	return user

def get_user_smile(db, user_data): # что бы не вылетело ошибки и смайл переназначился
	if not 'smile' in user_data: # если ключа smile нет, то мы ее берем из конфига
		user_data['smile'] = choice(settings.USER_EMOJI) # use_aliases добавляем - потому что у смайлов есть несколько вариантов обозначений
		db.users.update_one( # сохранение в бд
			{'_id': user_data['_id']}, # то что ищем, по _id ищем user_data['_id']
			{'$set': {'smile': user_data['smile']}} # устанавливаем поле smile м данными user_data['smile']
		)
	return emojize(user_data['smile'], use_aliases=True) # возврат пользователю

#  переключатель подписки и отписки
def toggle_subscription(db, user_data):
	if not user_data.get('subscribed'): # если не нету subscribed или переключатель False
		user_data['subscribed'] = True
	else: # если подписан
		user_data['subscribed'] = False
	db.users.update_one(
		{'_id': user_data['_id']},
		{'$set': {'subscribed': user_data['subscribed']}}
	)

# берем активных подписчиков 
def get_subscribers(db):
	return db.users.find({'subscribed': True})
