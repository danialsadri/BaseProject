from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, national_code, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('کاربر باید شماره تلفن داشته باشد')
        if not national_code:
            raise ValueError('کاربر باید کد ملی داشته باشد')
        user = self.model(phone_number=phone_number, national_code=national_code, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, national_code, password, **extra_fields):
        user = self.create_user(phone_number, national_code, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
