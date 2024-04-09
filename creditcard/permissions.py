from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class CanViewCreditCard(BasePermission):
    def has_permission(self, request, view):
        print("CAME")
        return request.user.has_perm('creditcard.view_creditcard')


class CanCreateCreditCard(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('creditcard.create_creditcard')
