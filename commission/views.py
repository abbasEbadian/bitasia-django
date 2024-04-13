from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.permissions import IsSuperUser
from bitpin.models import BitPinCurrency
from commission.models import WithdrawCommission
from commission.permissions import CommissionPermission
from commission.serializers import WithdrawCommissionSerializer, WithdrawCommissionUpdateSerializer, \
    WithdrawCommissionCreateSerializer


class WithdrawCommissionView(generics.ListCreateAPIView):
    queryset = WithdrawCommission.objects.all()
    permission_classes = [CommissionPermission]
    pagination_class = LimitOffsetPagination
    default_limit = 50

    @property
    def authentication_classes(self):
        return [] if self.request.method == 'GET' else [TokenAuthentication]

    def get_serializer_class(self):
        return WithdrawCommissionSerializer if self.request.method == 'GET' else WithdrawCommissionCreateSerializer

    @swagger_auto_schema(operation_id=_("Get Withdraw commission list"))
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": self.get_serializer(self.get_queryset(), many=True).data
        })

    @swagger_auto_schema(operation_id=_("Create new  Withdraw commission"))
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        newb = serializer.save()
        return Response({
            "result": "success",
            "object": WithdrawCommissionSerializer(newb).data
        })


class WithdrawCommissionDetailView(generics.RetrieveUpdateAPIView):
    queryset = WithdrawCommission.objects.all()
    lookup_field = "id"
    http_method_names = ["get", "patch"]
    permission_classes = [CommissionPermission]

    @property
    def authentication_classes(self):
        return [] if self.request.method == 'GET' else [TokenAuthentication]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WithdrawCommissionSerializer
        return WithdrawCommissionUpdateSerializer

    @swagger_auto_schema(operation_id=_("Get withdraw commission detail"))
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "object": self.get_serializer(self.get_object()).data
        })

    @swagger_auto_schema(operation_id=_("Update withdraw commission"))
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        newb = serializer.save()
        return Response({
            "result": "success",
            "object": WithdrawCommissionSerializer(newb).data
        })


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsSuperUser])
@swagger_auto_schema(operation_id="Generate withdraw commissions for each currency")
def generate_all_commissions(request):
    for curr in BitPinCurrency.objects.all().only("id"):
        for net in curr.network_ids.all().only("id"):
            WithdrawCommission.objects.get_or_create(currency_id=curr, network_id=net,
                                                     defaults={"amount": 0.01,
                                                               "type": WithdrawCommission.CommissionType.VALUE})

    return Response({
        "result": "success"
    })
