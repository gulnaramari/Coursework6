from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Класс разграничений по доступу для владельцев"""

    def has_object_permission(self, request, view, obj):
        """Метод для проверки прав доступа на объект."""

        if obj.owner == request.user:
            return True
        return False


class IsUserOwner(BasePermission):
    """Класс ограничений по доступу для ответственных за пользователя (владельцев)"""

    def has_object_permission(self, request, view, obj):
        """Метод для проверки прав доступа на объект."""

        if request.user == obj:
            return True
        return False
