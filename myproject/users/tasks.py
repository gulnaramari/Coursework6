from datetime import datetime
from celery import shared_task
from .services import send_message
from my_habbits.models import MyHabit


@shared_task
def send_habit_notification():
    """ Отправляет уведомление о выполнении привычки """
    hour_now = datetime.now().hour
    minute_now = datetime.now().minute
    habits = MyHabit.objects.filter(date_completion__hour=hour_now, date_completion__minute=minute_now)
    for habit in habits:
        award_or_related_habit = habit.award if habit.award else (
            habit.related_habit.name if habit.related_habit else "Никакого вознаграждения или связанной с ним привычки")
        message = f'''
    Ваша привычка {habit.name}:
    Действие: {habit.action},
    Место: {habit.place},
    Время: {habit.date_begin}
    Награда или приятная привычка: {award_or_related_habit}
    Время выполнения: {habit.habit_time}
'''
        send_message(message, habit.owner.tg_id)
        print(f'{habit.owner} - {habit.action} - {habit.place} отправить '
              f'{habit.owner} ({habit.owner.tg_nickname})')
