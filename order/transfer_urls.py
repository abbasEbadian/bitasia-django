from django.urls import path

from . import views

urlpatterns = [
    path('', views.TransferView.as_view(), name='transfer-list-create'),
    path('otp/', views.send_transfer_otp, name='transfer-otp'),
]
