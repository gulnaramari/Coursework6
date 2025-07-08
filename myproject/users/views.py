from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .permissions import IsUserOwner
from .serializer import (UserSerializer, UserBaseSerializer,
CreateUserBaseSerializer)


class UserListAPIView(generics.ListAPIView):
    """Контроллер-дженерик для списка пользователей."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер-дженерик для просмотра деталей пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Метод получения сериализатора в соответствии с запросом."""

        if (
                self.request.method == "GET"
                and self.get_object() != self.request.user
                or self.request.user.is_superuser is False
        ):
            return UserBaseSerializer
        if self.request.user.is_superuser:
            return UserSerializer
        return UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Контроллер-дженерик создания пользователя."""

    serializer_class = CreateUserBaseSerializer

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания
         пользователя с ограниченным доступом"""

        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    """Контроллер-дженерик для редактирования пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]


class UserDestroyAPIView(generics.DestroyAPIView):
    """Контроллер-дженерик для удаления пользователя."""

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]

