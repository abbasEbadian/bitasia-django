from django.urls import path
from .views import UserListView, UserDetailView, UserUpdateView, UserDeleteView

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user-delete"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="user-update"),
]
