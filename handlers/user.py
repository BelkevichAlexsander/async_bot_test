from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_config import bot, ID
from inline import user_ib
from message.user_message import MESSAGES


class FSMMessageAdmin(StatesGroup):
    """
    Машина состояний для формирования заказа по изготовлению бода
    """
    direction = State()
    platform = State()
    salary_start = State()
    salary_end = State()
    phone = State()


# @dp.callback_query_handler(lambda element: element.data and element.data.startswith('b'), state=FSMMessageAdmin)
async def call_back_application(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Получение результата (рекурсивно) из "Оставить заявку" -> "<следующие два выбора>" до ввода денег.
    Заполнение машинны состояния.
    :param callback_query: types.CallbackQuery
    :param state: FSMContext
    :return: продолжение формирования заявки
    """
    code = int(callback_query.data[-1])

    if code in [1, 2, 3]:
        async with state.proxy() as data:
            data['direction'] = callback_query.data[2:-2]

        await FSMMessageAdmin.next()
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=MESSAGES['platform'],
                                    reply_markup=user_ib.buttons_user2
                                    )

    if code in [4, 5, 6]:
        async with state.proxy() as data:
            data['platform'] = callback_query.data[2:-2]

        await FSMMessageAdmin.next()
        await bot.send_message(callback_query.message.chat.id, MESSAGES['start_budget'])


# @dp.message_handler(state=FSMMessageAdmin.salary_start)
async def start_price(message: types.Message, state: FSMContext):
    """
    Указание старта суммы для выполнения работы.
    Продолжение заполнения завки (Машины состояния)
    :param message: types.Message
    :param state: FSMContext
    :return: продолжение формирования заявки
    """
    async with state.proxy() as data:
        data['salary_start'] = message.text

    await FSMMessageAdmin.next()
    await bot.send_message(message.chat.id, 'До... "Ведите сумму"')


# price
# @dp.message_handler(state=FSMMessageAdmin.salary_end)
async def end_price(message: types.Message, state: FSMContext):
    """
    Указание максимальной суммы для выполнения работы.
    Продолжение заполнения завки (Машины состояния)
    :param message: types.Message
    :param state: FSMContext
    :return: продолжение формирования заявки
    """
    async with state.proxy() as data:
        data['salary_end'] = message.text

    await FSMMessageAdmin.next()
    await bot.send_message(message.chat.id, text='Введите номер телефона')


# @dp.message_handler(state=FSMMessageAdmin.phone)
async def phone(message: types.Message, state: FSMContext):
    """
    Получение и полное заполнение Машины состояни.
    Отправка пользователю сообщения об обработке заявки.
    Отправка результатов ввода пользователя админу.
    :param message: types.Message
    :param state: FSMContext
    :return: возврат в стартовое меню
    """
    async with state.proxy() as data:
        data['phone'] = message.text

    await state.finish()
    await bot.send_message(message.chat.id, text=MESSAGES['end'], reply_markup=user_ib.buttons_user_menu)
    await bot.send_message(chat_id=ID[0],
                           text=f'Клиент:\n '
                                f'id: {message.from_user.id}\n '
                                f'Имя: {message.from_user.first_name}\n\n'
                                f'Заказ:\n'
                                f'Направление бизнеса: {data["direction"]}\n'
                                f'Платформа чат-бота: {data["platform"]}\n\n'
                                f'Бюджет:\n'
                                f'От: {data["salary_start"]}\n'
                                f'До: {data["salary_end"]}\n\n'
                                f'Телефон: {data["phone"]}'
                           )


# Регистрация для выноса в MAIN
def registration_handler_user(dp: Dispatcher):
    dp.register_callback_query_handler(call_back_application,
                                       lambda c: c.data and c.data.startswith('b'),
                                       state=FSMMessageAdmin
                                       )
    dp.register_message_handler(start_price, state=FSMMessageAdmin.salary_start)
    dp.register_message_handler(end_price, state=FSMMessageAdmin.salary_end)
    dp.register_message_handler(phone, state=FSMMessageAdmin.phone)
