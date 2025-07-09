from datetime import time, timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import MyHabit


User = get_user_model()


class HabitTestCase(APITestCase):
    """Тесты для работы с привычками."""

    @classmethod
    def setUpTestData(cls):
        """Метод класса с начальными данными для тестов."""
        cls.user = User.objects.create(email="test@test.com")
        cls.habit = MyHabit.objects.create(
            name="Тест привычки",
            place="Где-нибудь",
            date_begin="04:20:00",
            action="Что-нибудь",
            is_pleasanthabit=False,
            period=4,
            award="Что-нибудь",
            habit_time=timedelta(seconds=90),
            is_publichabit=True,
            owner=cls.user,
            related_habit=None,
        )

    def setUp(self):
        """Задает начальные данные для тестов."""
        self.client.force_authenticate(user=self.user)

    def create_habit(self, **kwargs):
        """Создает привычку с заданными аргументами (или по умолчанию)."""
        defaults = {
            "name": "Тест привычки",
            "place": "Где-нибудь",
            "date_begin": "04:20:00",
            "action": "Что-нибудь",
            "is_pleasanthabit": False,
            "period": 4,
            "award": "Что-нибудь",
            "habit_time": timedelta(seconds=90),
            "is_publichabit": True,
            "owner": self.user,
            "related_habit": None,
        }
        defaults.update(kwargs)
        return MyHabit.objects.create(**defaults)

    def test_habit_create(self):
        """Тест создания новой привычки."""
        url = reverse("my_habbits:adding_habit")
        response = self.client.post(
            url,
            {
                "name": "Тест привычки",
                "place": "Дом",
                "date_begin": "07:40:00",
                "action": "Сделать уборку в комнате",
                "is_pleasanthabit": False,
                "period": 4,
                "award": "Пойти на концерт",
                "habit_time": "00:01:30",
                "is_publichabit": True,
                "owner": self.user.id,
                "related_habit": "",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MyHabit.objects.count(), 2)
        self.assertEqual(MyHabit.objects.last().name, "Тест привычки")
        self.assertEqual(MyHabit.objects.last().place, "Дом")
        self.assertEqual(MyHabit.objects.last().date_begin, time(7, 40))
        self.assertEqual(MyHabit.objects.last().action, "Сделать уборку в комнате")
        self.assertEqual(MyHabit.objects.last().is_pleasanthabit, False)
        self.assertEqual(MyHabit.objects.last().period, 4)
        self.assertEqual(MyHabit.objects.last().award, "Пойти на концерт")
        self.assertEqual(MyHabit.objects.last().habit_time, timedelta(seconds=90))
        self.assertEqual(MyHabit.objects.last().is_publichabit, True)
        self.assertEqual(MyHabit.objects.last().owner, self.user)
        self.assertEqual(MyHabit.objects.last().related_habit, None)

    def test_habit_list(self):
        """Тест на получение списка привычек."""
        url = reverse("my_habbits:habits")
        habit_1 = self.create_habit(name="Habit 1", place="Place 1")
        habit_2 = self.create_habit(name="Habit 2", place="Place 2")

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 3)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])

        expected_results = [
            {
                "id": self.habit.id,
                "name": self.habit.name,
                "place": self.habit.place,
                "date_begin": "04:20:00",
                "action": self.habit.action,
                "is_pleasanthabit": self.habit.is_pleasanthabit,
                "period": self.habit.period,
                "award": self.habit.award,
                "habit_time": "00:01:30",
                "is_publichabit": self.habit.is_publichabit,
                "owner": self.user.id,
                "related_habit": self.habit.related_habit,
            },
            {
                "id": habit_1.id,
                "name": "Habit 1",
                "place": "Place 1",
                "date_begin": "04:20:00",
                "action": "Гулять с собакой",
                "is_pleasanthabit": False,
                "period": 4,
                "award": "Мороженое",
                "habit_time": "00:01:30",
                "is_publichabit": True,
                "owner": self.user.id,
                "related_habit": None,
            },
            {
                "id": habit_2.id,
                "name": "Habit 2",
                "place": "Place 2",
                "date_begin": "04:20:00",
                "action": "Посуду помыть",
                "is_pleasanthabit": False,
                "period": 4,
                "award": "Денежка",
                "habit_time": "00:01:30",
                "is_publichabit": True,
                "owner": self.user.id,
                "related_habit": None,
            },
        ]
        self.assertCountEqual(data["results"], expected_results)

    def test_habit_retrieve(self):
        """Тест получения привычки по 'pk'"""
        url = reverse("my_habbits:habit", kwargs={"pk": self.habit.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "id": self.habit.id,
            "name": self.habit.name,
            "place": self.habit.place,
            "date_begin": self.habit.date_begin,
            "action": self.habit.action,
            "is_pleasanthabit": self.habit.is_pleasanthabit,
            "period": self.habit.period,
            "award": self.habit.award,
            "habit_time": "00:01:30",
            "is_publichabit": self.habit.is_publichabit,
            "owner": self.user.id,
            "related_habit": self.habit.related_habit,
        }
        self.assertEqual(response.data, expected_data)

    def test_habit_update(self):
        """Тест изменения привычки по Primary Key."""
        url = reverse("my_habbits:update_habit", kwargs={"pk": self.habit.id})
        updated_data = {
            "name": "Updated Habit",
            "place": "Somewhere",
            "date_begin": "05:30:00",
            "action": "Something",
            "is_pleasanthabit": False,
            "period": 2,
            "award": "Something",
            "habit_time": "00:02:00",
            "is_publichabit": False,
            "owner": self.user.id,
            "related_habit": None,
        }
        response = self.client.put(url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.name, updated_data["name"])
        self.assertEqual(self.habit.place, updated_data["place"])
        self.assertEqual(self.habit.date_begin, time(hour=5, minute=30))
        self.assertEqual(self.habit.action, updated_data["action"])
        self.assertEqual(self.habit.is_pleasanthabit, updated_data["is_pleasanthabit"])
        self.assertEqual(self.habit.period, updated_data["period"])
        self.assertEqual(self.habit.award, updated_data["award"])
        self.assertEqual(self.habit.habit_time, timedelta(seconds=120))
        self.assertEqual(self.habit.is_publichabit, updated_data["is_publichabit"])
        self.assertEqual(self.habit.owner.id, updated_data["owner"])
        self.assertEqual(self.habit.related_habit, updated_data["related_habit"])

    def test_habit_delete(self):
        """Тест удаления привычки """
        url = reverse("my_habbits:delete_habit", kwargs={"pk": self.habit.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MyHabit.objects.filter(id=self.habit.id).exists())
