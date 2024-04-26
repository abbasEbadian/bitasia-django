from django.db.transaction import atomic
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.permissions import IsModerator
from .models import JibitRequest
from .serializers import JibitSerializer, JibitCreateSerializer


class JibitView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsModerator]
    queryset = JibitRequest.objects.all()
    pagination_class = LimitOffsetPagination
    default_limit = 50

    def get_queryset(self):
        user_id = self.request.GET.get("user_id", None)
        if user_id:
            return JibitRequest.objects.filter(user_id=user_id)
        return self.queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return JibitSerializer
        return JibitCreateSerializer

    @swagger_auto_schema(operation_id=_("Get Jibit Requests"))
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": self.get_serializer(self.get_queryset(), many=True).data
        })

    @swagger_auto_schema(operation_id=_("New request for user or card"))
    def post(self, request, *args, **kwargs):
        with atomic():
            serializer = JibitCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "result": "success",
                "message": _("Request sent to Jibit, Result will be available soon.")
            })
