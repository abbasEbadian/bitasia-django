from django.urls import path

from . import views

urlpatterns = [
    path('', views.TransactionView.as_view(), name='transaction-list-create'),
    path('<int:id>', views.TransactionDetailView.as_view(), name='transaction-detail-update'),
    # path('purchase/', views.PurchaseView.as_view(), name='purchase-list-create'),
    # path('purchase/confirm/', views.PurchaseAdminConfirmView.as_view(), name='purchase-confirm')
]
