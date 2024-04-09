from django.urls import path

from . import views

urlpatterns = [
    path("", views.WithdrawCommissionView.as_view(), name="withdraw-commission-list-create"),
    path("<int:id>", views.WithdrawCommissionDetailView.as_view(), name="withdraw-commission-detail-update"),
    path("generate_all_commissions/", views.generate_all_commissions, name="generate-commissions"),
]
