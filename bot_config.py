import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import config

loop = asyncio.get_event_loop()
storage = MemoryStorage()

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(bot=bot, storage=storage, loop=loop)  # (bot=bot, storage=storage) if MemoryStorage

ID = [
    int(config.id_admin_telegram_1.get_secret_value()),
    # int(config.config.id_admin_telegram_2.get_secret_value())
    ]

PAYMENT_TOKEN = config.PAYMENTS_TOKEN.get_secret_value()

ITEM_URL = config.ITEMS_URL.get_secret_value()
