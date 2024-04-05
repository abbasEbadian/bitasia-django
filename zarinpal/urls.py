from django.urls import path

from . import views

urlpatterns = [
    path('callback/', views.payment_callback, name='gateway_callback'),
    path('deposit/new/', views.create_rial_deposit, name='create_rial_deposit'),
    path('deposit/', views.RialDepositView.as_view(), name='payment_history'),
    path('withdraw/', views.RialWithdrawView.as_view(), name='rial_payment-list-create'),
    path('withdraw/manage/', views.RialWithdrawConfirmView.as_view(), name='rial_payment-manage'),
]
