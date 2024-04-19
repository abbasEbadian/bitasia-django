from django.db.transaction import atomic
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import IsModeratorMixin
from api.permissions import IsModerator
from ticket.models import Ticket
from ticket.permissions import TicketPermission
from ticket.serializers import TicketSerializer, TicketCreateSerializer, TicketAddMessageSerializer


class TicketView(generics.ListCreateAPIView, IsModeratorMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [(IsAuthenticated & ~IsModerator) | (IsModerator & TicketPermission)]

    def get_queryset(self):
        if self.is_moderator(self.request):
            return Ticket.objects.all()
        return Ticket.objects.filter(user_id=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TicketSerializer
        return TicketCreateSerializer

    @swagger_auto_schema(operation_id=_("Ticket list"))
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": TicketSerializer(self.get_queryset(), many=True).data
        })

    @swagger_auto_schema(operation_id=_("Create new ticket"))
    def post(self, request, *args, **kwargs):
        with atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            ticket = serializer.save(user_id=request.user)
            return Response({
                "result": "success",
                "object": TicketSerializer(ticket).data
            })


class TicketDetailView(generics.ListCreateAPIView, IsModeratorMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [(IsAuthenticated & ~IsModerator) | (IsModerator & TicketPermission)]
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        if self.is_moderator(self.request):
            return Ticket.objects.all()
        return Ticket.objects.filter(user_id=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TicketSerializer
        return TicketAddMessageSerializer

    @swagger_auto_schema(operation_id=_("Ticket detail"))
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "object": TicketSerializer(self.get_object(), many=True).data
        })

    @swagger_auto_schema(operation_id=_("Update detail"))
    def patch(self, request, *args, **kwargs):
        with atomic():
            serializer = self.get_serializer(self.get_object(), data=request.data)
            serializer.is_valid(raise_exception=True)
            ticket = serializer.save(user_id=request.user, is_moderator=self.is_moderator(self.request))
            return Response({
                "result": "success",
                "object": TicketSerializer(ticket).data
            })

    @swagger_auto_schema(operation_id=_("Close ticket"))
    def delete(self, request, *args, **kwargs):
        with atomic():
            instance = self.get_object()
            instance.status = Ticket.Status.CLOSED
            instance.save()
            return Response({
                "result": "success",
                "object": TicketSerializer(instance).data
            })
