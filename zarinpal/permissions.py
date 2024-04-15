from rest_framework.permissions import DjangoModelPermissions


class RialWithdrawPermission(DjangoModelPermissions):
    authenticated_users_only = True

    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
    }


class RialDepositPermission(DjangoModelPermissions):
    authenticated_users_only = True

    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
    }
