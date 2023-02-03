from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# button menu start
button_application = InlineKeyboardButton(text='Оставить заявку', callback_data='menu_1')
button_buy = InlineKeyboardButton(text='Купить товар', callback_data='menu_2')
button_balance = InlineKeyboardButton(text='Мой баланс', callback_data='menu_3')
button_admin = InlineKeyboardButton(text='Отправить сообщение пользователям', callback_data='menu_4')

# button menu 1.1
button_sell = InlineKeyboardButton(text='Продажа', callback_data='b_Продажа_1')
button_production = InlineKeyboardButton(text='Производство', callback_data='b_Производство_2')
button_service = InlineKeyboardButton(text='Оказание услуг', callback_data='b_Оказание услуг_3')

# button menu 1.2
button_telegram = InlineKeyboardButton(text='Телеграмм', callback_data='b_Телеграмм_4')
button_whatsapp = InlineKeyboardButton(text='Ватсап', callback_data='b_Ватсап_5')
button_viber = InlineKeyboardButton(text='Вайбер', callback_data='b_Вайбер_6')

# button menu 2.1
button_sold_1 = InlineKeyboardButton(text='Купить 1 раз', callback_data='sold_1')
button_sold_2 = InlineKeyboardButton(text='Купить 2 раза', callback_data='sold_2')

# menu user
buttons_user_menu = InlineKeyboardMarkup(row_width=1)
buttons_user_menu.add(button_application, button_buy, button_balance)

# menu admin
buttons_admin_menu = InlineKeyboardMarkup(row_width=1)
buttons_admin_menu.add(button_application, button_buy, button_balance, button_admin)

# menu 1.1
buttons_user1 = InlineKeyboardMarkup(row_width=1)
buttons_user1.add(button_sell, button_production, button_service)

# menu 1.2
buttons_user2 = InlineKeyboardMarkup(row_width=1)
buttons_user2.add(button_telegram, button_whatsapp, button_viber)

# menu 2.1
buttons_sold = InlineKeyboardMarkup(row_width=1)
buttons_sold.add(button_sold_1, button_sold_2)
