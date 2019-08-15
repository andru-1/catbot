from pymongo import MongoClient
import settings

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