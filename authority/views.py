from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import IsModeratorMixin
from api.permissions import IsModerator
from authority.models import AuthorityLevel, AuthorityRule, AuthorityRuleOption, AuthorityRequest
from authority.permissions import AuthorityLevelPermission, AuthorityRulePermission, AuthorityRuleOptionPermission, \
    AuthorityRequestPermission
from authority.serializer import AuthorityLevelSerializer, AuthorityRuleWithOptionSerializer, \
    AuthorityRequestSerializer, AuthorityRequestUpdateSerializer


class AuthorityLevelView(generics.ListAPIView):
    serializer_class = AuthorityLevelSerializer
    queryset = AuthorityLevel.objects.all()
    permission_classes = [(IsModerator & AuthorityLevelPermission) | permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_id="Get authority levels", tags=["Authority"])
    def get(self, request, *args, **kwargs):
        return Response(AuthorityLevelSerializer(self.get_queryset(), many=True).data)

    def paginator(self):
        return False


class AuthorityRulesView(generics.ListAPIView):
    permission_classes = [(IsModerator & AuthorityRulePermission) | permissions.IsAuthenticatedOrReadOnly]
    serializer_class = AuthorityRuleWithOptionSerializer
    queryset = AuthorityRule.objects.all()

    @swagger_auto_schema(operation_id="Get authority rules", tags=["Authority"])
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "objects": serializer.data
        })


class AuthorityRuleOptionsView(generics.ListAPIView):
    permission_classes = [(IsModerator & AuthorityRuleOptionPermission) | permissions.IsAuthenticatedOrReadOnly]
    serializer_class = AuthorityRuleWithOptionSerializer
    queryset = AuthorityRuleOption.objects.all()

    @swagger_auto_schema(operation_id="Get authority rule options", tags=["Authority"])
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "objects": serializer.data
        })


class AuthorityRuleView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorityRuleWithOptionSerializer
    queryset = AuthorityRule.objects.all()

    @swagger_auto_schema(operation_id="Get single authority rule", tags=["Authority"])
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "result": "success",
            "object": serializer.data
        })


class AuthorityRequestView(generics.ListAPIView, IsModeratorMixin):
    permission_classes = [(IsAuthenticated & ~IsModerator) | (IsModerator & AuthorityRequestPermission)]
    serializer_class = AuthorityRuleWithOptionSerializer
    queryset = AuthorityRule.objects.all()

    def get_queryset(self):
        if self.is_moderator(self.request):
            return AuthorityRequest.objects.all()
        return AuthorityRequest.objects.select_related("user_id").filter(user_id=self.request.user)

    @swagger_auto_schema(operation_id="Get single authority rule", tags=["Authority"])
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "result": "success",
            "object": serializer.data
        })


class AuthorityRequestDetailView(generics.RetrieveUpdateAPIView, IsModeratorMixin):
    authentication_classes = [TokenAuthentication]
    http_method_names = ["get", "patch"]
    permission_classes = [(IsAuthenticated & ~IsModerator) | (IsModerator & AuthorityRequestPermission)]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AuthorityRequestSerializer
        return AuthorityRequestUpdateSerializer

    def get_queryset(self):
        if self.is_moderator(self.request):
            return AuthorityRequest.objects.all()
        return AuthorityRequest.objects.select_related("user_id").filter(user_id=self.request.user)

    @swagger_auto_schema(operation_id="Get single authority rule", tags=["Authority"])
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            "result": "success",
            "object": serializer.data
        })

    @swagger_auto_schema(operation_id="Accept/Reject single authority request", tags=["Authority"])
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({
            "result": "success",
            "object": AuthorityRequestSerializer(instance).data
        })
