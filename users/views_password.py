from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.schema import forget_password_change_view_schema, reset_password_change_view_schema
from users.serializers_password import VerifyForgetPasswordSerializer, VerifyResetPasswordSerializer


@swagger_auto_schema(**forget_password_change_view_schema)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def forget_password_change_view(request):
    serializer = VerifyForgetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({
        "result": "success",
        "message": _('Password changed successfully')
    })


@swagger_auto_schema(**reset_password_change_view_schema)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reset_password_change_view(request):
    serializer = VerifyResetPasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({
        "result": "success",
        "message": _('Password changed successfully')
    })
