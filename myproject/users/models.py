from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    """Класс менеджера для создания объектов модели "Пользователь"."""

    def create_user(self, email, password=None, **extra_fields):
        """Кастомная модель пользователя"""

        if not email:
            raise ValueError("Укажите адрес электронной почты")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Метод создания объекта "суперпользователь" модели "Пользователь"."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Модель пользователя"""

    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    avatar = models.ImageField(
        upload_to="users/images",
        null=True,
        blank=True,
        verbose_name="Аватар профиля"

    )
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name="Номер телефона")
    city = models.CharField(max_length=100, blank=True, verbose_name="Город")
    username = None
    token = models.CharField(max_length=150, blank=True, null=True, verbose_name="Токен для верификации")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата последнего изменения")
    tg_nickname = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='Имя пользователя в Telegram',
        blank=True,
        null=True
    )
    tg_id = models.CharField(
        max_length=50,
        verbose_name='ID пользователя в Telegram',
        blank=True,
        null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """Метод отображения в строковом виде модели "Пользователь"."""

        return self.email

    class Meta:
        """Класс для изменения поведения полей модели "Пользователь"."""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email", "tg_nickname", "updated_at"]
