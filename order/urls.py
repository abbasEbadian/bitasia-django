from django.urls import path

from . import views

urlpatterns = [
    path('', views.TransactionView.as_view(), name='transaction-list-create'),
    # path('purchase/', views.PurchaseView.as_view(), name='purchase-list-create'),
    # path('purchase/confirm/', views.PurchaseAdminConfirmView.as_view(), name='purchase-confirm')
]
