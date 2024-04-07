from django.urls import path

from . import views

urlpatterns = [
    path('', views.PermissionView.as_view(), name='permission-list'),
    path('groups/', views.GroupView.as_view(), name="group-list")
]
