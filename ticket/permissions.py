from rest_framework.permissions import DjangoModelPermissions


class TicketPermission(DjangoModelPermissions):
    authenticated_users_only = True

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
    }
