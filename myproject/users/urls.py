from django.urls import path
from .apps import UsersConfig
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from .views import (UserListAPIView, UserRetrieveAPIView, UserCreateAPIView,
UserUpdateAPIView, UserDestroyAPIView)

app_name = UsersConfig


urlpatterns = [
    path("", UserListAPIView.as_view(), name="profiles"),
    path("profile/<int:pk>/", UserRetrieveAPIView.as_view(), name="profile"),
    path("registration/", UserCreateAPIView.as_view(), name="registration"),
    path("profile/<int:pk>/update/", UserUpdateAPIView.as_view(), name="update_profile"),
    path("profile/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="delete_profile"),
    path("authorization/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="authorization"),
    path("refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
]

