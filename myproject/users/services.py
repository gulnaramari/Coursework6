import requests
from requests import RequestException

from .settings import TG_TOKEN, TG_URL

tg_token = TG_TOKEN


def send_message(text, chat_id):
    """ Отправляет сообщение через Telegram-бота"""
    params = {
        'text': text,
        'chat_id': chat_id
    }
    try:
        response = requests.get(f'{TG_URL}{tg_token}/sendMessage', params=params)
        response.raise_for_status()
    except RequestException as e:
        print(f'Ошибка: {e}')
