from django.urls import path
from .apps import MyHabbitsConfig
from .views import (
    MyHabitCreateAPIView,
    MyHabitListAPIView,
    MyHabitRetrieveAPIView,
    MyHabitUpdateAPIView,
    MyHabitDestroyAPIView,
)


app_name = MyHabbitsConfig.name

urlpatterns = [
    path("habits/", MyHabitListAPIView.as_view(), name="habits"),
    path("habit/<int:pk>/", MyHabitRetrieveAPIView.as_view(), name="habit"),
    path("habit/new/", MyHabitCreateAPIView.as_view(), name="adding_habit"),
    path("habit/<int:pk>/update/", MyHabitUpdateAPIView.as_view(), name="update_habit"),
    path(
        "habit/<int:pk>/delete/", MyHabitDestroyAPIView.as_view(), name="delete_habit"
    ),
]
