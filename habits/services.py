import requests
from telebot import logger

from config import settings


def send_telegram_message(chat_id, message):
    """
       Отправляет сообщение в Telegram.
    """
    params = {
        "text": message,
        "chat_id": chat_id
    }
    url = f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, json=params, timeout=10)

    if response.status_code != 200:
        logger.error(f"Ошибка при отправке сообщения в Telegram: {response.text}")
        raise Exception("Ошибка при отправке сообщения!")
    else:
        logger.info(f"Сообщение успешно отправлено пользователю с ID {chat_id}.")
        return response
