from django.urls import path

from referral.views import ReferralProgramView, ReferralProgramDetailView, get_user_referral_income

urlpatterns = [
    path("", ReferralProgramView.as_view(), name="referral-list-create"),
    path("<int:pk>/", ReferralProgramDetailView.as_view(), name="referral-update-delete"),
    path("incomes/", get_user_referral_income)
]
