from django.db.transaction import atomic
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.mixins import IsModeratorMixin
from api.permissions import IsModerator, IsSimpleUser
from notification.models import Notification
from notification.permissions import NotificationPermission
from notification.serializers import NotificationSerializer, NotificationCreateSerializer, \
    NotificationSeenUpdateSerializer, NotificationAdminSerializer


class NotificationView(generics.ListCreateAPIView, IsModeratorMixin):
    authentication_classes = [TokenAuthentication]
    pagination_class = LimitOffsetPagination
    default_limit = 30

    @property
    def permission_classes(self):
        if self.request.method == "GET":
            return [IsSimpleUser | (IsModerator & NotificationPermission)]
        return [IsModerator, NotificationPermission]

    def get_serializer_class(self):
        if self.request.method == "GET":
            if self.is_moderator(self.request):
                return NotificationAdminSerializer
            return NotificationSerializer
        return NotificationCreateSerializer

    def get_queryset(self):
        if self.is_moderator(self.request):
            return Notification.objects.all()
        return Notification.objects.for_user(self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    @swagger_auto_schema(operation_id=_("Get notification list"))
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": self.get_serializer(self.get_queryset(), many=True).data
        })

    @swagger_auto_schema(operation_id=_("Create new notification"), operation_summary="Admin only")
    def post(self, request, *args, **kwargs):
        with atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            Notification.objects.create_for_users(users=data["users"], title=data["title"],
                                                  content=data["content"])
            return Response({
                "result": "success"
            }, status=status.HTTP_201_CREATED)


class NotificationSeenView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSimpleUser]
    http_method_names = ["patch"]
    serializer_class = NotificationSeenUpdateSerializer

    @swagger_auto_schema(operation_id=_("Update notification(s) seen"))
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        for notif in data["notifications"]:
            notif.seen_user_ids.add(request.user)
        return Response({
            "result": "success"
        })
