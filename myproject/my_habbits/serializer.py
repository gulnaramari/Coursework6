from rest_framework import serializers
from .models import MyHabit
from datetime import timedelta
from .validators import (
    AwardOrRelatedValidator,
    HabitTimeValidator,
    PleasantValidator,
    PublicPleasantValidator,
    FrequencyValidator,
    RelatedPublicValidator,
    RelatedOwnerValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    """Класс сериализатора к модели привычка"""

    class Meta:
        model = MyHabit
        fields = "__all__"


class DurationFieldSerializer(serializers.DurationField):
    """Кастомный сериализатор для поля длительности."""

    def to_representation(self, value):
        """Метод для отображения поля в обычном виде."""
        if not value:
            return None
        total_seconds = int(value.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def to_internal_value(self, data):
        """Метод для вывода времени в виде интервала."""
        try:
            parts = list(map(int, data.split(":")))
            if len(parts) == 3:
                return timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2])
            elif len(parts) == 2:
                return timedelta(minutes=parts[0], seconds=parts[1])
            raise serializers.ValidationError(
                'Недопустимый формат времени. Используйте "ЧЧ:ММ:СС" или "ММ:СС".'
            )
        except (ValueError, TypeError):
            raise serializers.ValidationError("Недопустимый формат времени")


class HabitBaseSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор для модели привычки с дополнительными полями,
    касающимися связанной привычки."""

    habit_time = DurationFieldSerializer(help_text="Формат: ЧЧ:ММ:СС или MM:SS")
    related_habit = HabitSerializer(read_only=True)
    related_habit_id = serializers.PrimaryKeyRelatedField(
        queryset=MyHabit.objects.all(),
        source="related_habit",
        write_only=True,
        allow_null=True,
        default=None,
    )

    class Meta:
        model = MyHabit
        fields = [
            "id",
            "name",
            "place",
            "date_begin",
            "action",
            "is_pleasanthabit",
            "period",
            "award",
            "habit_time",
            "is_publichabit",
            "owner",
            "related_habit",
            "related_habit_id",
        ]
        validators = [
            AwardOrRelatedValidator("related_habit", "award"),
            HabitTimeValidator("habit_time"),
            PleasantValidator("related_habit"),
            PublicPleasantValidator("is_pleasanthabit", "award", "related_habit"),
            FrequencyValidator("periodicity"),
            RelatedPublicValidator("related_habit", "is_publichabit"),
            RelatedOwnerValidator("related_habit", "owner"),
        ]
