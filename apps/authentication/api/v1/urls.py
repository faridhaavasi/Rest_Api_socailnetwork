from django.urls import path
from apps.authentication.api.v1.views.register_signup_views import SeteEailApiView

urlpatterns = [
    path('setemail', SeteEailApiView.as_view(), name='set_email')
]