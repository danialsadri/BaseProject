from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from apps.accounts.models import User


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username='', password=None, **kwargs):
        try:
            user = User.objects.get(Q(phone_number=username) | Q(national_code=username), is_active=True)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
