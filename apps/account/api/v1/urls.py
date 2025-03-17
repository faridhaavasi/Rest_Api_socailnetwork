from django.urls import path
from apps.account.api.v1.views.profile_views import GetProfileView

urlpatterns = [
    path('profile/', GetProfileView.as_view(), name='get_profile'),
]   
