from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authority.models import AuthorityLevel, AuthorityRule
from authority.serializer import AuthorityLevelSerializer, AuthorityRuleWithOptionSerializer


class AuthorityLevelView(generics.GenericAPIView):
    serializer_class = AuthorityLevelSerializer
    permission_classes = [IsAuthenticated]
    queryset = AuthorityLevel.objects.all()

    @swagger_auto_schema(operation_id="Get authority levels", tags=["authority"])
    def get(self, request, *args, **kwargs):
        return Response(AuthorityLevelSerializer(self.get_queryset(), many=True).data)

    def paginator(self):
        return False


class AuthorityRulesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorityRuleWithOptionSerializer
    queryset = AuthorityRule.objects.all()

    @swagger_auto_schema(operation_id="Get authority rules", tags=["authority"])
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "objects": serializer.data
        })

    def paginator(self):
        return False


class AuthorityRuleView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorityRuleWithOptionSerializer
    queryset = AuthorityRule.objects.all()

    @swagger_auto_schema(operation_id="Get single authority rule", tags=["authority"])
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "result": "success",
            "object": serializer.data
        })

    def paginator(self):
        return False
