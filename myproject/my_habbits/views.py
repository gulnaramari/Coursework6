from rest_framework import generics
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .models import MyHabit
from .paginator import HabitPaginator
from .serializer import HabitBaseSerializer
from users.permissions import IsOwner


class MyHabitListAPIView(generics.ListAPIView):
    """Контроллер-дженерик для списка привычек."""

    serializer_class = HabitBaseSerializer
    queryset = MyHabit.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        """Метод для изменения запроса к базе данных по объектам модели "Привычки"."""

        user = self.request.user
        if user.is_authenticated:
            return MyHabit.objects.filter(Q(owner=user) | Q(is_public=True)).order_by(
                "id"
            )
        else:
            return MyHabit.objects.filter(is_public=True).order_by("id")


class MyHabitRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер-дженерик для просмотра привычки."""

    serializer_class = HabitBaseSerializer
    queryset = MyHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class MyHabitCreateAPIView(generics.CreateAPIView):
    """Контроллер-дженерик для создания привычки."""

    serializer_class = HabitBaseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Привычки"."""

        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class MyHabitUpdateAPIView(generics.UpdateAPIView):
    """Контроллер-дженерик для изменения привычки."""

    serializer_class = HabitBaseSerializer
    queryset = MyHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class MyHabitDestroyAPIView(generics.DestroyAPIView):
    """Контроллер-дженерик для удаления привычки."""

    queryset = MyHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
