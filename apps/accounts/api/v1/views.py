from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SendCodeSerializer, LoginSerializer


class SendCodeApiView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=SendCodeSerializer)
    def post(self, request):
        data = self.request.data
        serializer = SendCodeSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            otp_code = serializer.check_user()
            response = {
                'phone_number': data.get('phone_number'),
                'message': 'کد احرازهویت با موفقیت ارسال شد',
            }
            return Response(data=response, status=status.HTTP_200_OK)


class LoginApiView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer)
    def post(self, request):
        data = self.request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.verify_code()
            refresh = RefreshToken.for_user(user)
            response = {
                'user': user.id,
                'message': 'با موفقیت وارد شدید',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(response, status=status.HTTP_201_CREATED)
