from django.urls import path
from apps.account.api.v1.views.profile_views import GetProfileView
from apps.account.api.v1.views.follow_views import FollowUserApiView
app_name = 'account_v1'
urlpatterns = [
    path('profile/', GetProfileView.as_view(), name='get_profile'),
    path('follow/<int:user_id>/', FollowUserApiView.as_view(), name='follow_user'),

]   
