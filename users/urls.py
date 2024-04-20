from django.urls import path

from authentication.views import forget_password_view
from .views import UserListView, LoginHistoryView, UserDetailView
from .views_password import forget_password_change_view, reset_password_change_view

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("history/", LoginHistoryView.as_view(), name="login-history-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail-update"),
    # path("create/", UserCreateView.as_view(), name="user-create"),
    path("forget-password/otp/", forget_password_view, name="forget-password-otp"),
    path("forget-password/", forget_password_change_view, name="forget-password-save"),
    path("reset-password/", reset_password_change_view, name="reset-password-save"),
]
