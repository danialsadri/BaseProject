from django.urls import path, include

app_name = 'api-v1'
urlpatterns = [
    path('accounts/', include('apps.accounts.api.v1.urls', namespace='accounts')),
    path('utils/', include('apps.utils.api.v1.urls', namespace='utils')),
]
