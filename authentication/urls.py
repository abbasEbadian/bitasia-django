from django.urls import path

from . import views

urlpatterns = [
    # path('login/', views.LoginView.as_view(), name='login')
    path("login/", views.CreateOTPView.as_view(), name="login"),
    path("otp/verify/", views.LoginView.as_view(), name="verify-otp"),
    path("register/", views.RegisterView.as_view(), name="register"),
    # path("register/", ),
    # path("reset-password/", ),
]
