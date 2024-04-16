from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, DjangoModelPermissions

User = get_user_model()


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        pk = view.kwargs.get('pk')
        return bool(request.user.id == pk)


class LoginHistoryPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
    }
