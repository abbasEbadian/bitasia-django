from django.contrib.auth import get_user_model
from rest_framework.permissions import DjangoModelPermissions

User = get_user_model()


class CreditCardPermission(DjangoModelPermissions):
    authenticated_users_only = True

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.add_%(model_name)s'],
    }
