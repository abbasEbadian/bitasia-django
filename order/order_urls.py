from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderView.as_view(), name='orders-list-create'),
    path('<int:id>', views.OrderDetailView.as_view(), name='order-detail'),
    path("calculate-buysell-commission/", views.CalculateOrderCommissionView.as_view(),
         name='calculate-buysell-commission'),

]
