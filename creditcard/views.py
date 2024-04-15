from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.response import Response

from api.mixins import IsModeratorMixin
from api.permissions import IsOwner, IsSimpleUser
from creditcard.models import CreditCard
from creditcard.permissions import CreditCardPermission
from creditcard.schema import creditcard_create_schema
from creditcard.serializers import CreditCardCreateSerializer, CreditCardSerializer, CreditCardUpdateSerializer


class CreditCardView(generics.ListCreateAPIView, IsModeratorMixin):
    authentication_classes = (TokenAuthentication,)
    lookup_field = "id"

    @property
    def permission_classes(self):
        if self.request.method == "GET":
            return [CreditCardPermission]
        return [IsSimpleUser]

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return CreditCardSerializer
        return CreditCardCreateSerializer

    def get_queryset(self):
        if self.is_moderator(self.request):
            return CreditCard.objects.all()
        return CreditCard.objects.filter(user_id=self.request.user.id)

    @swagger_auto_schema(operation_id=_("Get credit cards of current user"))
    def get(self, request):
        objects = self.get_serializer(self.get_queryset(), many=True).data
        return Response({
            "result": "success",
            "objects": objects
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(**creditcard_create_schema)
    def post(self, request):
        serializer = CreditCardCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        serializer.save(user_id=user)

        return Response({
            "result": "success"
        }, status.HTTP_201_CREATED)


class CreditCardDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView, IsModeratorMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [CreditCardPermission | IsOwner]
    http_method_names = ["patch", "delete", "get"]
    lookup_field = "id"

    @swagger_auto_schema(operation_id="Get credit card detail")
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "object": self.get_serializer(self.get_object()).data
        })

    def get_queryset(self):
        if self.is_moderator(self.request):
            return CreditCard.objects.all()
        return CreditCard.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return CreditCardSerializer
        return CreditCardUpdateSerializer

    @swagger_auto_schema(operation_id="Update existing credit card", security=[{"Token": []}])
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, context={"partial": True})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "result": "success",
            "message": _("Successfully updated credit card  ")
        }, status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="Delete existing credit card", security=[{"Token": []}])
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            "result": "success",
            "message": _("Successfully deleted credit card")
        })
