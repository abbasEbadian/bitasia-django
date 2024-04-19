from django.urls import path

from ticket import views

urlpatterns = [
    path("", views.TicketView.as_view(), name="ticket-list-create"),
    path("<int:pk>/", views.TicketDetailView.as_view(), name="ticket-detail-update-close"),
]
