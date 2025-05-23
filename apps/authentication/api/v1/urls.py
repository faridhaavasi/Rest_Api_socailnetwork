from django.urls import path
from apps.authentication.api.v1.views.register_signup_views import (
    SeteEailApiView, 
    ConfirmEmailApiView,
    SetPasswordApiView,
    RestorePasswordApiView,
    RestorePasswordConfirmApiView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('setemail', SeteEailApiView.as_view(), name='set_email'),
    path('confirmemail/<str:value_token>', ConfirmEmailApiView.as_view(), name='confirm_email'),
    path('setpassword', SetPasswordApiView.as_view(), name='set_password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('restorepassword', RestorePasswordApiView.as_view(), name='restore_password'),
    path('restorepasswordconfirm/<str:value>', RestorePasswordConfirmApiView.as_view(), name='restore_password_confirm'),
]