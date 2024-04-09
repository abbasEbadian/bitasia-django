from django.urls import path

from . import views

urlpatterns = [
    path('', views.TransactionView.as_view(), name='transaction-list-create'),
    path('<int:id>', views.TransactionDetailView.as_view(), name='transaction-detail-update'),
    path("calculate-commission/", views.calculate_commission, name='calculate-commission'),
]
