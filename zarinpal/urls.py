from django.urls import path

from . import views

urlpatterns = [
    path('create_rial_payment/', views.create_rial_deposit, name='create_rial_payment'),
    path('callback/', views.payment_callback, name='create_rial_payment'),
    path('payment/history/', views.RialDepositView.as_view(), name='payment_history'),
    path('rial_withdraw/', views.RialWithdrawView.as_view(), name='rial_payment-list-create'),
    path('rial_withdraw/manage/', views.RialWithdrawConfirmView.as_view(), name='rial_payment-manage'),
]
