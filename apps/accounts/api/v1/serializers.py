import random
from django.core.cache import cache
from django.utils import timezone
from rest_framework import serializers
from apps.accounts.models import UserModel
from apps.utils.validators import validate_phone, validate_otp_code
from config.error_manager import ErrorHandler


class SendCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[validate_phone])

    def send_code(self):
        phone_number = self.validated_data.get('phone_number')
        otp_code = random.randint(1000, 9999)
        send_time = timezone.now()
        cache.set(f'user-{phone_number}', {'otp_code': otp_code, 'send_time': send_time})
        print({'otp_code': otp_code, 'send_time': send_time})
        # send_sms_thread(phone_number, otp_code)
        return otp_code

    def check_user(self):
        phone_number = self.validated_data.get('phone_number')
        try:
            user = UserModel.objects.get(phone_number=phone_number)
            if user.is_active:
                return self.send_code()
            else:
                raise ErrorHandler.get_error_exception(400, 'not_is_active')
        except UserModel.DoesNotExist:
            return self.send_code()


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[validate_phone])
    otp_code = serializers.IntegerField(validators=[validate_otp_code])

    def verify_code(self):
        phone_number = self.validated_data.get('phone_number')
        otp_code = self.validated_data.get('otp_code')
        time = timezone.now()
        user_cache = cache.get(f'user-{phone_number}')
        if user_cache and (time - user_cache.get('send_time')).total_seconds() <= 120:
            if user_cache.get('otp_code') == otp_code:
                cache.delete(f'user-{phone_number}')
                user, is_created = UserModel.objects.get_or_create(phone_number=phone_number)
                user.login_time = timezone.now()
                user.save()
                return user, is_created
            raise ErrorHandler.get_error_exception(400, 'invalid_otp_code')
        raise ErrorHandler.get_error_exception(400, 'expired_otp_code')


class ReSendCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[validate_phone])

    def send_code(self):
        phone_number = self.validated_data.get('phone_number')
        otp_code = random.randint(1000, 9999)
        send_time = timezone.now()
        cache.set(f'user-{phone_number}', {'otp_code': otp_code, 'send_time': send_time})
        print({'otp_code': otp_code, 'send_time': send_time})
        # send_sms_thread(phone_number, otp_code)
        return otp_code

    def check_user(self):
        phone_number = self.validated_data.get('phone_number')
        try:
            user = UserModel.objects.get(phone_number=phone_number)
            if user.is_active:
                return self.send_code()
            else:
                raise ErrorHandler.get_error_exception(400, 'not_is_active')
        except UserModel.DoesNotExist:
            return self.send_code()


class UserDetailsSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        if obj.photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.photo.image.url)
        else:
            return None

    class Meta:
        model = UserModel
        fields = [
            'id', 'phone_number', 'email', 'first_name', 'last_name',
            'photo', 'login_time', 'is_active', 'is_staff', 'is_superuser',
            'created_at', 'updated_at',
        ]
