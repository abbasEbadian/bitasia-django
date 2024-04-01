from django.urls import path

from . import views

urlpatterns = [
    path('', views.CurrencyView.as_view(), name='currency-list'),
    path('networks/', views.NetworkView.as_view(), name='network-list')
]
