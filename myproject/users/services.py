import json
from datetime import datetime

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from my_habbits.models import MyHabit


def create_replacements(habit: MyHabit) -> dict[str, str | list[str]]:
    """Словарь замещений"""
    m = datetime.fromisoformat(habit.time).time().minute
    h = x = datetime.fromisoformat(habit.time).time().hour
    y = datetime.fromisoformat(habit.end_time).time().hour if habit.end_time else 0
    z = (x + y) // 2
    d = ",".join([day.day for day in habit.days_of_week.all()]) if habit.days_of_week else "d"
    return {"m": str(m), "x": str(x), "y": str(y), "z": str(z), "h": str(h), "d": d}


def make_replacements(text: str, replacements: dict) -> str:
    """Replaces vars in text with correct values."""
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def create_schedule(crontab: str) -> CrontabSchedule:
    """Создание расписания для периодической задачи """
    minute, hour, day_of_month, month_of_year, day_of_week = crontab.split()
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute=minute,
        hour=hour,
        day_of_week=day_of_week,
        day_of_month=day_of_month,
        month_of_year=month_of_year,
    )
    return schedule


def create_task(schedule: CrontabSchedule, habit: Habit) -> None:
    """Создание периодической задачи"""
    PeriodicTask.objects.create(
        crontab=schedule,
        name=f"посылаю напоминание {habit.pk}",
        task="habits.tasks.send_message",
        args=json.dumps([habit.pk]),
    )
