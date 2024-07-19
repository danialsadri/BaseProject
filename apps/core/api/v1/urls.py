from django.urls import path, include

urlpatterns = [
    path('accounts/', include('apps.accounts.api.v1.urls')),
    path('utils/', include('apps.utils.api.v1.urls')),
]
