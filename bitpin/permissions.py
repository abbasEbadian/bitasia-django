from rest_framework.permissions import DjangoModelPermissions

CHANGE_PERM = '%(app_label)s.change_%(model_name)s'
CREATE_PERM = '%(app_label)s.add_%(model_name)s'
DELETE_PERM = '%(app_label)s.delete_%(model_name)s'
VIEW_PERM = '%(app_label)s.view_%(model_name)s'


class BitPinCurrencyPermission(DjangoModelPermissions):
    authenticated_users_only = False

    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'PATCH': [CHANGE_PERM],
    }


class BitPinNetworkPermission(DjangoModelPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [CREATE_PERM],
        'PATCH': [CHANGE_PERM],
    }


class WalletAddressPermission(DjangoModelPermissions):
    authenticated_users_only = True

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [CREATE_PERM],
        'PATCH': [CHANGE_PERM],
        'DELETE': [CREATE_PERM]
    }
