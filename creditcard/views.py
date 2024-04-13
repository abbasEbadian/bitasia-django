from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response

from api.permissions import IsOwner
from creditcard.models import CreditCard
from creditcard.schema import creditcard_create_schema
from creditcard.serializers import CreditCardCreateSerializer, CreditCardSerializer


class CreditCardView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return CreditCardSerializer
        return CreditCardCreateSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
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


class CreditCardDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser, DjangoModelPermissions]
    http_method_names = ["patch", "delete", "get"]
    queryset = CreditCard.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(operation_id="Get credit card detail")
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "object": self.get_serializer(self.get_object()).data
        })

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return CreditCardSerializer
        return CreditCardCreateSerializer

    @swagger_auto_schema(operation_id="Update existing credit card", security=[{"Token": []}])
    def patch(self, request, id):
        serializer = CreditCardCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        instance = self.get_object()
        instance = CreditCard.objects.filter(id=instance.id)
        instance.update(**serializer.validated_data)

        return Response({
            "result": "success",
            "message": _("Successfully updated credit card  ")
        }, status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="Delete existing credit card", security=[{"Token": []}])
    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        return Response({
            "result": "success",
            "message": _("Successfully deleted credit card")
        })
