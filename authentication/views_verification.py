from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
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
from jibit.models import JibitRequest

User = get_user_model()


def get_national_url(user_id, filename):
    ext = filename.split('.')[-1]
    return ["images/users/%d" % user_id, "national_card.%s" % ext]


class VerifyAccountView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyAccountSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer, ]

    @swagger_auto_schema(**verify_account_schema)
    def post(self, request, *args, **kwargs):
        user = self.request.user
        rule_id = int(request.data.get('rule_id'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cuser = User.objects.filter(pk=user.pk)
        rule_id = AuthorityRule.objects.filter(pk=rule_id).first()
        if not cuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        req, created = AuthorityRequest.objects.get_or_create(rule_id=rule_id, user_id=user)

        if "national_card_image" in serializer.validated_data:
            file = serializer.validated_data.pop('national_card_image')
            path, name = get_national_url(user.id, file.name)
            fs = FileSystemStorage(location="media/" + path)
            f = fs.save(name, file)
            url = fs.url(f).replace("/media", "")
            cuser.update(national_card_image=path + url)

        cuser.update(**serializer.validated_data)
        if "national_code" in serializer.validated_data:
            JibitRequest.objects.create(user_id=user, type=JibitRequest.Type.NATIONAL_WITH_MOBILE).send_request()
        return Response(
            {
                "result": "success",
                "message": _('Updated successfully, Our team will check your information ASAP.')
            },
            status=status.HTTP_200_OK, content_type="application/json")
