from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response

from api.const import MODERATOR_FIELD, MODERATOR_VALUE
from api.permissions import IsModerator, IsSimpleUser
from referral.models import ReferralProgram
from referral.permissions import ReferralProgramPermission
from referral.serializers import ReferralProgramSerializer, ReferralProgramCreateSerializer


class ReferralProgramView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsModerator, ReferralProgramPermission]
    queryset = ReferralProgram.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReferralProgramSerializer
        return ReferralProgramCreateSerializer

    @swagger_auto_schema(operation_id=_("Referral program list"))
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": self.get_serializer(self.get_queryset(), many=True).data
        })

    @swagger_auto_schema(operation_id=_("Referral program create"))
    def post(self, request, *args, **kwargs):
        serializer = ReferralProgramCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({
            "result": "success",
            "object": ReferralProgramSerializer(instance).data
        })


class ReferralProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsModerator, ReferralProgramPermission]
    queryset = ReferralProgram.objects.all()
    http_method_names = ["patch", "delete"]
    serializer_class = ReferralProgramCreateSerializer

    @swagger_auto_schema(operation_id=_("Update referral program"))
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({
            "result": "success",
            "object": ReferralProgramSerializer(instance).data
        })

    @swagger_auto_schema(operation_id=_("Delete referral program"))
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "result": "success"
        })


@swagger_auto_schema(operation_id=_("Get user referral program"), method="GET",
                     operation_description="Must send user referral code if admin is requesting",
                     manual_parameters=[
                         openapi.Parameter(name="referral", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
                     ])
@api_view(["GET"])
@authentication_classes(TokenAuthentication)
@permission_classes([IsSimpleUser | (IsModerator & ReferralProgramPermission)])
def get_user_referral_income(request, *args, **kwargs):
    user = request.user
    referral = request.GET.get("referral")
    is_moderator = request.META.get(MODERATOR_FIELD) == MODERATOR_VALUE
    if not is_moderator:
        incomes = user.get_referral_incomes()
    if not referral:
        pass
    return Response({
        "result": "success",
        "objects": []
    })
