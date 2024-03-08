from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import IndividualUser

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = IndividualUser.objects.get(Q(email=username) | Q(phone=username))
        except IndividualUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
    
