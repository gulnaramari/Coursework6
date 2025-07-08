from datetime import timedelta
from django.db import models
from users.models import User


class MyHabit(models.Model):
    """ Модель привычки"""
    name = models.CharField(max_length=400, verbose_name='Наименование привычки', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец привычки', blank=True, null=True)
    place = models.CharField(max_length=280, verbose_name='Место', blank=True, null=True)
    date_begin = models.TimeField(verbose_name='Дата начала выполнения', blank=True, null=True)
    action = models.CharField(max_length=280, verbose_name='Действие', blank=True, null=True)
    is_pleasanthabit = models.BooleanField(default=False, verbose_name='Приятная привычка')
    is_publichabit = models.BooleanField(default=False, verbose_name='Привычка опубликована')
    period = models.PositiveSmallIntegerField(default=7, verbose_name="Периодичность привычки")
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная привычка',
                                      related_name='related_habits', blank=True, null=True)

    award = models.CharField(max_length=100, verbose_name='Вознаграждение', blank=True, null=True)
    habit_time = models.DurationField(default=timedelta(seconds=120), verbose_name='Время на привычку')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        if self.owner:
            return f'{self.owner.email} - {self.action} - {self.place} '
        return f'Нет владельца, ответственного за привычку: {self.action} - {self.place}'
