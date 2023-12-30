from django.urls import path

from .views import UserListView, UserDetailView, UserUpdateView, UserDeleteView, UserCreateView, UserDetailAdminView

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailAdminView.as_view(), name="user-detail-admin"),
    path("detail/", UserDetailView.as_view(), name="user-detail"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user-delete"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="user-update"),
    path("create/", UserCreateView.as_view(), name="user-create"),
]
