from django.urls import path

from . import views

urlpatterns = [
    path('', views.JibitView.as_view(), name='jibit-request-list-create'),
]
