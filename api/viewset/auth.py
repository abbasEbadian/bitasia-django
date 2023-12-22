from rest_framework import viewsets
from django.contrib.auth import get_user_model
from api.serializer.auth import UserSerializer
User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
