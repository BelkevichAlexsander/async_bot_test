import logging
from aiogram.utils import executor

from bot_config import dp
from handlers import user, admin, you_kassa, menu_start
from database import sqlite_db


logging.basicConfig(level=logging.INFO)


async def on_startup(_):
	print('Бот вышел в онлайн')
	sqlite_db.sql_start()

	you_kassa.registration_payments(dp=dp)
	user.registration_handler_user(dp=dp)
	menu_start.registration_handler_start_menu(dp=dp)
	admin.registration_handler_admin(dp=dp)

if __name__ == '__main__':
	executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
