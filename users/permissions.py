from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Разрешение, которое позволяет владельцу объекта выполнять любые действия,
    а остальным пользователям — только чтение.
    """
    def has_object_permission(self, request, view, obj):
        """
        Проверяет, является ли пользователь владельцем объекта.
        """
        return obj.owner == request.user
