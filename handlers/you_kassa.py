from aiogram import Dispatcher, types
from aiogram.types import Message, ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType

from message.payments_message import MESSAGES
from bot_config import bot, PAYMENT_TOKEN, ITEM_URL, ID


FAST_SHIPPING_OPTION = ShippingOption(
    id='speed',
    title='Быстрая даставка!'
).add(LabeledPrice('При встрече', 100000))


POST_SHIPPING_OPTION = ShippingOption(
    id='post',
    title='ЕвроПочта'
)

POST_SHIPPING_OPTION.add(LabeledPrice('Кортонная коробка', 10000))
POST_SHIPPING_OPTION.add(LabeledPrice('Срочное отправление!', 10000))

PICKUP_SHIPPING_OPTION = ShippingOption(
    id='pickup',
    title='Самовывоз'
)

PICKUP_SHIPPING_OPTION.add(LabeledPrice('Самовывоз в Минске', 1000))


# @dp.callback_query_handler(lambda element: element.data and element.data.startswith('sold'))
async def buy_process(callback_query: types.CallbackQuery):
    """
    Обработка выбора покупки товара и вызов оплаты
    :param callback_query: types.CallbackQuery
    :return: меню оплаты товара
    """
    prices = [LabeledPrice(label='Кросовки', amount=45000)]
    if callback_query.data[-1] == "2":
        prices = [
            LabeledPrice(label='Кросовки', amount=45000),
            LabeledPrice(label='Кросовки', amount=45000)
        ]

    await bot.send_invoice(callback_query.message.chat.id,
                           title=MESSAGES['item_title'],
                           description=MESSAGES['item_description'],
                           provider_token=PAYMENT_TOKEN,
                           currency='rub',
                           photo_url=ITEM_URL,
                           photo_height=512,
                           photo_width=512,
                           photo_size=512,
                           need_email=True,
                           need_phone_number=True,
                           is_flexible=False,
                           prices=prices,
                           start_parameter='example',
                           payload='some_invoice')


# @dp.shipping_query_handler(lambda q: True)
async def shipping_process(shipping_query: ShippingQuery):
    """
        Проверка на доставку в страну заказчика
        :param shipping_query: ShippingQuery
        :return: продолжение заполнения данных для оплаты товара
    """

    # проверка на доставку в Австралию с отказом
    if shipping_query.shipping_address.country_code == 'AU':
        return await bot.answer_shipping_query(
            shipping_query.id,
            ok=False,
            error_message=MESSAGES['AU_error']
        )

    # shipping_options = [FAST_SHIPPING_OPTION]
    #
    # # Дотавка европочтой
    # if shipping_query.shipping_address.country_code == 'BYN':
    #     shipping_options.append(POST_SHIPPING_OPTION)
    #
    #     # Доставка самовывозом
    #     if shipping_query.shipping_address.city == 'Минск':
    #         shipping_options.append(PICKUP_SHIPPING_OPTION)

    # Ответ
    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
    )


# Проверка оплаты
# @dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    """
    Проверка оплаты товара.
    :param pre_checkout_query: PreCheckoutQuery
    :return: удачную оплату
    """
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    """
    Отправка сообщения об оплате
    :param message: Message
    :return: сообщение админу об успешной оплате
    """
    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(total_amount=message.successful_payment.total_amount // 100,
                                              currency=message.successful_payment.currency)
    )
    await bot.send_message(ID[0], message.successful_payment)


# Регистрация для выноса в MAIN
def registration_payments(dp: Dispatcher):
    dp.register_callback_query_handler(buy_process, lambda element: element.data and element.data.startswith('sold'))
    dp.register_shipping_query_handler(shipping_process, lambda q: True)
    dp.pre_checkout_query_handler(checkout_process, lambda q: True)
    dp.message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
