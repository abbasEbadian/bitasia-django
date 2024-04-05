from django.urls import path

from . import views

urlpatterns = [
    path('', views.WalletView.as_view(), name='wallet-list-create'),
    path('<int:id>/', views.WalletDetailView.as_view(), name='wallet-detail'),
]
