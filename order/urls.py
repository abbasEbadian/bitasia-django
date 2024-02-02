from django.urls import path

from order import views

urlpatterns = [
    path('create_rial_payment/', views.create_rial_deposit, name='create_rial_payment'),
    path('callback/', views.payment_callback, name='create_rial_payment')
]
