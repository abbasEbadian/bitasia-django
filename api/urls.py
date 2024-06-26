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
    path('permissions/', include('permission.urls'), name='permissions'),
    path('orders/', include('order.order_urls'), name='orders'),
    path('transfers/', include('order.transfer_urls'), name='transfers'),
    path('commisions/', include('commission.urls'), name='commissions'),
    path('tickets/', include('ticket.urls'), name='tickets'),
    path('jibit-requests/', include('jibit.urls'), name='jibit-requests'),
    path('referrals/', include('referral.urls'), name='referrals'),
    path('notifications/', include('notification.urls'), name='notifications'),
]
