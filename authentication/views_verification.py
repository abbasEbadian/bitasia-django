from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from authentication.schema import verify_account_schema
from authentication.serializer import VerifyAccountSerializer
from authority.models import AuthorityRequest, AuthorityRule

User = get_user_model()


class VerifyAccountView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyAccountSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer, ]

    @swagger_auto_schema(**verify_account_schema)
    def put(self, request, *args, **kwargs):
        user = self.request.user
        rule_id = int(request.data.get('rule_id'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cuser = User.objects.filter(pk=user.pk)
        rule_id = AuthorityRule.objects.filter(pk=rule_id).first()
        if not cuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        req, created = AuthorityRequest.objects.get_or_create(rule_id=rule_id, user_id=user, approved=False)
        # TODO: what if already had request
        cuser.update(**serializer.validated_data)

        return Response(
            {
                "result": "success",
                "message": _('Updated successfully, Our team will check your information ASAP.')
            },
            status=status.HTTP_200_OK, content_type="application/json")
