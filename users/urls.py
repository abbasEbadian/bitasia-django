from django.urls import path

from authentication.views import forget_password_view
from .views import UserListView, UserDetailView, UserUpdateView, UserDeleteView, UserCreateView, UserDetailAdminView, \
    LoginHistoryView, forget_password_change_view

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("history/", LoginHistoryView.as_view(), name="login-history-list"),
    path("<int:pk>/", UserDetailAdminView.as_view(), name="user-detail-admin"),
    path("detail/", UserDetailView.as_view(), name="user-detail"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user-delete"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="user-update"),
    path("create/", UserCreateView.as_view(), name="user-create"),
    path("forget-password/otp/", forget_password_view, name="forget-password-otp"),
    path("forget-password/", forget_password_change_view, name="forget-password-save"),
]
