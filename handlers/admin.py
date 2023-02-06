from aiogram import types, Dispatcher
from aiogram.utils.exceptions import BotBlocked

from bot_config import bot, ID
from database import sqlite_db
from inline import user_ib


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
            try:
                await bot.send_message(ret[0], text=f'Уважаемый(ая) {ret[1]}.\n {message.text}')
            except BotBlocked:
                await message.answer(f"Blocked bot by {ret[1]}")
        await message.answer("Рассылка завершена!")
        await message.answer('Админ панель.', reply_markup=user_ib.buttons_admin_menu)


# Регистрация для выноса в MAIN
def registration_handler_admin(dp: Dispatcher):
    dp.register_message_handler(spent_all_message)
