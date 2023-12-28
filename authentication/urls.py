from django.urls import path
from . import views


urlpatterns = [
    # path('login/', views.LoginView.as_view(), name='login')
    path("otp/", views.CreateOTPView.as_view(), name="send-otp"),
    path("otp/verify/", views.LoginView.as_view(), name="verify-otp"),
    # path("register/", ),
    # path("reset-password/", ),
]