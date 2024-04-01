from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderView.as_view(), name='order-list'),
    # path('networks/', views.NetworkView.as_view(), name='network-list')
]
