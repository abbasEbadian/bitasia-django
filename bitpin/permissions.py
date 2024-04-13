from rest_framework.permissions import DjangoModelPermissions


class BitPinCurrencyPermission(DjangoModelPermissions):
    authenticated_users_only = False

    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
    }
