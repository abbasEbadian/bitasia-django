from django.urls import path, include

urlpatterns = [
    path('auth/', include('authentication.urls'), name='authentication'),
    path('users/', include('users.urls'), name='users'),
    path('authority/', include('authority.urls'), name='authority'),
    path('creditcards/', include('creditcard.urls'), name='creditcard'),
    path('currencies/', include('bitpin.urls'), name='currency'),
    path('transactions/rial/', include('zarinpal.urls'), name='rial-transactions'),
    path('transactions/crypto/', include('order.urls'), name='crypto-transactions'),
    path('wallets/', include('wallet.urls'), name='crypto-transactions'),
    # path('orders/', include('order.urls'), name='transactions'),
]
