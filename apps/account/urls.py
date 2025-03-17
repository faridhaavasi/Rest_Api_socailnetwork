from django.urls import path, include

app_name = 'account'

urlpatterns = [
    path('api/v1/', include('apps.account.api.v1.urls'), name='account-v1'),
]