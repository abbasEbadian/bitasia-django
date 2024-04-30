from django.urls import path

from . import views

urlpatterns = [
    path("", views.NotificationView.as_view(), name="notification-list-create"),
    path("update-seen/", views.NotificationSeenView.as_view(), name="notification-update-seen")
]
