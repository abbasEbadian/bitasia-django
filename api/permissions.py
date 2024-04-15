from rest_framework.permissions import BasePermission, IsAdminUser

from api.const import MODERATOR_FIELD, MODERATOR_VALUE


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


# is staff and has x-role header = "moderator"
class IsModerator(IsAdminUser):
    def has_permission(self, request, view):
        admin = super().has_permission(request, view)
        return admin and request.headers.get(MODERATOR_FIELD, None) == MODERATOR_VALUE


class IsSimpleUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_staff
