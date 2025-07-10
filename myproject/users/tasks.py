import requests
from celery import shared_task
from my_habbits.models import MyHabit
from config.settings import TG_TOKEN


@shared_task
def send_message(pk) -> None:
    """Посылка напоминания через тг-бота """
    habit = MyHabit.objects.get(pk=pk)
    text = (
        f"Сейчас время для {habit.action} в конкретном месте: {habit.place}! "
        f"Не забудь потом принять награду:{habit.award if habit.award else habit.related_habit}!"
    )
    params = {
        "text": text,
        "chat_id": habit.user.tg_id,
    }
    requests.get(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", params=params)

