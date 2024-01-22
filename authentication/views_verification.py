from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from authentication.schema import verify_account_step1_schema
from authentication.serializer import VerifyAccountSerializer

User = get_user_model()


class VerifyAccountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyAccountSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer, ]

    @swagger_auto_schema(**verify_account_step1_schema)
    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cuser = User.objects.filter(pk=user.pk)
        data = {"first_name": serializer.validated_data.get("first_name"),
                "last_name": serializer.validated_data.get("last_name"),
                "gender": serializer.validated_data.get("gender"),
                "birthdate": serializer.validated_data.get("birthdate"),
                serializer.validated_data.get('image_name') + "_image": serializer.validated_data.get('image')}
        cuser.update(**data)

        return Response(
            {
                "result": "success",
                "message": _('Updated successfully')
            },
            status=status.HTTP_200_OK, content_type="application/json")
