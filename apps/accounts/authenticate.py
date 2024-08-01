from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from apps.accounts.models import UserModel


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username='', password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(phone_number=username) | Q(email=username), is_active=True)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
