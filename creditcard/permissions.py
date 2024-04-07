from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from .models import CreditCard

User = get_user_model()


class IsCreditCardOwner(BasePermission):

    def has_permission(self, request, view):
        pk = view.kwargs.get('id')
        obj = get_object_or_404(CreditCard, pk=pk)
        return bool(request.user == obj.user_id)


class CanViewCreditCard(BasePermission):
    def has_permission(self, request, view):
        print("CAME")
        return request.user.has_perm('creditcard.view_creditcard')


class CanCreateCreditCard(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('creditcard.create_creditcard')
