from django.urls import path

from . import views

urlpatterns = [
    path('', views.CreditCardView.as_view(), name='credit-card'),
    path('<int:id>/', views.CreditCardDeleteUpdateView.as_view(), name='credit-card-update')
]
