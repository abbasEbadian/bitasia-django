from django.urls import path, include

urlpatterns = [
    path('auth/', include('authentication.urls'), name='authentication'),
    path('users/', include('users.urls'), name='users'),
    path('authority/', include('authority.urls'), name='authority'),
]
