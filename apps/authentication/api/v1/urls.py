from django.urls import path
from apps.authentication.api.v1.views.register_signup_views import (
    SeteEailApiView, 
    ConfirmEmailApiView,
    SetPasswordApiView,
)

urlpatterns = [
    path('setemail', SeteEailApiView.as_view(), name='set_email'),
    path('confirmemail/<str:token>', ConfirmEmailApiView.as_view(), name='confirm_email'),
    path('setpassword', SetPasswordApiView.as_view(), name='set_password'),
]