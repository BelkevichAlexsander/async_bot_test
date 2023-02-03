from aiogram import types, Dispatcher

from bot_config import bot, ID
from database import sqlite_db


# @dp.message_handler()
async def spent_all_message(message: types.Message):
    """
    Функция только для админа.
    Делает выборку из бд всех пользователей и рассылает им отловленное сообщение от админа.
    :param message: types.Message
    :return: Сообщение всем пользователям от админа
    """
    if message.from_user.id in ID:
        read = await sqlite_db.message_all_user('user')
        for ret in read:
            await bot.send_message(ret[0], text=f'Уважаемый(ая) {ret[1]}.\n {message.text}')


# Регистрация для выноса в MAIN
def registration_handler_admin(dp: Dispatcher):
    dp.register_message_handler(spent_all_message)
