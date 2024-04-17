from rest_framework.permissions import DjangoModelPermissions


class OrderPermission(DjangoModelPermissions):
    authenticated_users_only = True

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
    }


class TransactionPermission(DjangoModelPermissions):
    authenticated_users_only = True

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
    }


class TransferPermission(DjangoModelPermissions):
    authenticated_users_only = True

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
    }
