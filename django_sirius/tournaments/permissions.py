import rest_framework.permissions as permissions


class UserAdminPermission(permissions.BasePermission):
    _safe_methods = ['GET', 'HEAD', 'OPTIONS']

    def has_permission(self, request, view):
        # Разрешить все запросы от аутентифицированных пользователей
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешить безопасные методы всем
        if request.method in self._safe_methods:
            return True
        # Разрешить запросы от владельца объекта или администратора
        return obj.owner == request.user or request.user.is_staff
