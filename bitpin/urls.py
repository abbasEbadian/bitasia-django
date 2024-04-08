from django.urls import path

from . import views

urlpatterns = [
    path('', views.CurrencyView.as_view(), name='currency-list'),
    path('<int:id>/', views.CurrencyDetailView.as_view(), name='currency-detail'),
    path('networks/', views.NetworkView.as_view(), name='network-list'),
    path('wallets/', views.WalletAddressView.as_view(), name='wallet-address'),
    path('wallets/<int:id>', views.WalletAddressDetailView.as_view(), name='wallet-address-deta')
]
