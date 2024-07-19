from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView, TokenBlacklistView,
)
from . import views

app_name = 'accounts_api'
urlpatterns = [
    path('send-code/', views.SendCodeApiView.as_view(), name='send-code'),
    path('token/', views.LoginApiView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
