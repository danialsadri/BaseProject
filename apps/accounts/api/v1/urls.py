from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenBlacklistView
from . import views

app_name = 'accounts'
urlpatterns = [
    path('send-code/', views.SendCodeApiView.as_view(), name='send-code'),
    path('token/', views.LoginApiView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('resend-code/', views.ResendCodeApiView.as_view(), name='resend-code'),
    path('user-details/', views.UserDetailsApiView.as_view(), name='user-details'),
]
