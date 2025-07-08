from rest_framework import serializers
from .models import MyHabit
from datetime import timedelta



class HabitSerializer(serializers.ModelSerializer):
    """ Класс сериализатора к модели привычка """

    class Meta:
        model = MyHabit
        fields = '__all__'


class HabitBaseSerializer(serializers.ModelSerializer):
    """ Кастомный сериализатор для модели привычки с дополнительными полями,
     касающимися связанной привычки. """
    related_habit = HabitSerializer(read_only=True)
    related_habit_id = serializers.PrimaryKeyRelatedField(
        queryset=MyHabit.objects.all(),
        source='related_habit',
        write_only=True,
        allow_null=True,
        default=None
    )

    class Meta:
        model = MyHabit
        fields = [
            'id', 'name', 'place', 'date_begin', 'action', 'is_pleasanthabit',
            'period', 'award', 'execution_time', 'is_publichabit', 'owner',
            'related_habit', 'related_habit_id'
        ]
