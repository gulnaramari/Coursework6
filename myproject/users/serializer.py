from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователя."""

    class Meta:
        model = User
        fields = ["avatar", "email", "tg_nickname", "tg_id", "city"]


class UserBaseSerializer(serializers.ModelSerializer):
    """Класс сериализатора с ограниченным доступом к модели пользователя."""

    class Meta:
        model = User
        fields = ["avatar", "email", "city"]


class CreateUserBaseSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор для создания пользователя с ограниченным доступом."""

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """Класс для изменения поведения полей сериализатора"""

        model = User
        fields = ["avatar", "email", "city", "password"]
