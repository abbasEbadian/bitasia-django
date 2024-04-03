from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderView.as_view(), name='order-list-create'),
    path('purchase/', views.PurchaseView.as_view(), name='purchase-list-create'),
    path('purchase/confirm/', views.PurchaseAdminConfirmView.as_view(), name='purchase-confirm')
]
