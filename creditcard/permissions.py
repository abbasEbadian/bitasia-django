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
