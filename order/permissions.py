from creditcard import permissions


class CanConfirmPurchase(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff
