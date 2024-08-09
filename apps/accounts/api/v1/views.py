from django.core.cache import cache
from django.utils import timezone
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SendCodeSerializer, LoginSerializer, UserDetailsSerializer, ReSendCodeSerializer


@method_decorator(ratelimit(key='user_or_ip', rate='3/1d', block=True), name='post')
class SendCodeApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = SendCodeSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data.get('phone_number')
            otp_code = serializer.check_user()
            response = {
                'phone_number': phone_number,
                'message': 'کد احرازهویت با موفقیت ارسال شد',
            }
            return Response(data=response, status=status.HTTP_200_OK)


@method_decorator(ratelimit(key='user_or_ip', rate='3/1d', block=True), name='post')
class LoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user, is_created = serializer.verify_code()
            refresh = RefreshToken.for_user(user)
            response = {
                'user': user.id,
                'is_created_first': is_created,
                'message': 'با موفقیت وارد شدید',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data=response, status=status.HTTP_201_CREATED)


@method_decorator(ratelimit(key='user_or_ip', rate='3/1d', block=True), name='post')
class ResendCodeApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = ReSendCodeSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data.get('phone_number')
            user_cache = cache.get(f'user-{phone_number}')
            if user_cache:
                if (timezone.now() - user_cache.get('send_time')).total_seconds() <= 120:
                    return Response(
                        data={'message': 'لطفاً کمی صبر کنید و سپس دوباره امتحان کنید'},
                        status=status.HTTP_429_TOO_MANY_REQUESTS
                    )
                otp_code = serializer.check_user()
                return Response(
                    data={'phone_number': phone_number, 'message': 'کد احرازهویت مجدداً ارسال شد'},
                    status=status.HTTP_200_OK
                )
            return Response(
                data={'message': 'کدی برای این شماره تلفن ارسال نشده است. لطفاً ابتدا درخواست کد کنید'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserDetailsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailsSerializer(instance=self.request.user, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
