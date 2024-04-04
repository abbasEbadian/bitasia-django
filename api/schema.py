from drf_yasg import openapi

create_payment_schema = {
    "method": "post",
    "operation_id": "Create Rial Transactions Link",
    "tags": ["Rial Transactions"],
    "request_body": openapi.Schema(type=openapi.TYPE_OBJECT,
                                   required=["amount", 'card_number'],
                                   properties={
                                       "amount": openapi.Schema(type=openapi.TYPE_NUMBER),
                                       "card_number": openapi.Schema(type=openapi.TYPE_STRING)
                                   }),
}
