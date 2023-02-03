from pydantic import BaseSettings, SecretStr
from dotenv import load_dotenv
import os


class Settings(BaseSettings):
    """
    Для подгрузки секретных ключей и иных значений
    """
    bot_token: SecretStr
    id_admin_telegram_1: SecretStr
    # id_admin_telegram_e2: SecretStr
    PAYMENTS_TOKEN: SecretStr
    ITEMS_URL: SecretStr

    class Config:
        """
        Вложенный класс с дополнительными указаниями для настроек.
        Получение данных из .env в переменные выше
        """
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            c = load_dotenv(dotenv_path)


# Валидация объекта конфига
config = Settings()
