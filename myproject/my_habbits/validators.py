from datetime import timedelta

from django.core.validators import BaseValidator
from rest_framework import serializers
from rest_framework.serializers import ValidationError


class BaseValidator:
    """Класс для проверок."""

    def __init__(self, *fields):
        """Инициализатор класса."""
        self.fields = fields

    def __call__(self, attrs):
        """Вызывается DRF для проверки."""
        field_values = {field: attrs.get(field) for field in self.fields}
        self.validate(**field_values)

    def validate(self, **kwargs):
        """Реализуется в дочерних классах."""
        raise NotImplementedError("Подклассы должны реализовывать этот метод.")


class AwardOrRelatedValidator(BaseValidator):
    """Исключает одновременный выбор соответствующей привычки и вознаграждения."""

    def validate(self, related_habit, award, **kwargs):
        if award and related_habit:
            raise serializers.ValidationError(
                "Приятная привычка не может иметь вознаграждения или связанной с ней привычки"
            )


class HabitTimeValidator(BaseValidator):
    """Проверяет время выполнения привычки."""

    def validate(self, habit_time, **kwargs):
        if habit_time and habit_time > timedelta(seconds=120):
            raise serializers.ValidationError(
                "Время выполнения должно составлять не более 120 секунд."
            )


class PleasantValidator(BaseValidator):
    """Проверяет, что привычка имеет атрибут "приятная привычка",
    чтобы ее выбрать как "связанная привычка"."""

    def validate(self, related_habit, **kwargs):
        if related_habit and not related_habit.is_pleasanthabit:
            raise serializers.ValidationError(
                "Выбранная привычка должна быть приятной привычкой!"
            )


class PublicPleasantValidator(BaseValidator):
    """Если текущая привычка имеет атрибут приятная, то нельзя указывать вознаграждение или связанную привычку"""

    def validate(self, is_pleasanthabit, award, related_habit, **kwargs):
        """Метод для проверки."""
        if is_pleasanthabit and (award or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть награды или связанной с ней привычки."
            )


class FrequencyValidator(BaseValidator):
    """Запрещается выполнять данную привычку реже, чем раз в 7 дней."""

    def validate(self, period, **kwargs):
        """Метод для проверки на периодичность выполнения привычки."""
        if period and not (1 <= period <= 7):
            raise serializers.ValidationError(
                "Периодичность выполнения привычки не может быть реже, чем раз в 7 дней."
            )


class RelatedPublicValidator(BaseValidator):
    """Подтверждает, что связанная привычка является общедоступной, если текущая привычка является общедоступной."""

    def validate(self, related_habit, is_publichabit, **kwargs):
        """Метод для проверки."""
        if related_habit and is_publichabit:
            if not related_habit.is_publichabit:
                raise serializers.ValidationError(
                    "Указанная связанная привычка должна быть общедоступной"
                )


class RelatedOwnerValidator(BaseValidator):
    """Подтверждает, что связанная привычка принадлежит тому же владельцу, что и текущая привычка."""

    def validate(self, related_habit, owner):
        """Метод для проверки, что связанная привычка создана владельцем текущей привычки"""
        if related_habit is not None and related_habit.owner != owner:
            raise serializers.ValidationError(
                "Указанная связанная привычка должна быть создана Вами."
            )

