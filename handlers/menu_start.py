from aiogram import types, Dispatcher

from bot_config import ID, bot
from database import sqlite_db
from handlers.user import FSMMessageAdmin
from inline import user_ib


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    """
    Вывод стартового меню.
    Разделение на меню админа и пользователя.
    Сохранение данных пользователя для дальнейшего подсчета денег и отправки общего сообщения от админа.
    :param message: types.Message
    :return: Возвращает стартовое меню в зависимости от статуса
    """
    if message.from_user.id in ID:
        await sqlite_db.sql_add_user(state=(message.from_user.id, message.from_user.first_name, 0, 'admin'))
        await message.answer(
            f'Hello admin {message.from_user.username}\n \tМеню',
            reply_markup=user_ib.buttons_admin_menu
        )
    else:
        await sqlite_db.sql_add_user(state=(message.from_user.id, message.from_user.first_name, 0, 'user'))
        await message.answer('Меню', reply_markup=user_ib.buttons_user_menu)

    await message.delete()


# @dp.callback_query_handler(lambda element: element.data and element.data.startswith('menu'))
async def call_back_head_menu(callback_query: types.CallbackQuery):
    """
    Получение результата выбора со стартового меню.
    Вывод результата выбора.
    :param callback_query: types.CallbackQuery
    :return: Возвращает результат в зависимости от выбора
    """
    code = int(callback_query.data[-1])

    if code == 1:
        await FSMMessageAdmin.direction.set()
        await callback_query.message.reply('Какое направление вашего бизнеса?', reply_markup=user_ib.buttons_user1)

    if code == 2:
        await callback_query.message.reply('Товар', reply_markup=user_ib.buttons_sold)

    if code == 3:
        read = await sqlite_db.sql_read_for_balance(callback_query.message.chat.id)
        await bot.send_message(read[0], text=f'У вас {read[2]} условных единиц')

    if code == 4:
        await bot.send_message(callback_query.message.chat.id,
                               text='Введи текст для всех пользователей Бота')


# Регистрация для выноса в MAIN
def registration_handler_start_menu(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_callback_query_handler(call_back_head_menu, lambda c: c.data and c.data.startswith('menu'))
