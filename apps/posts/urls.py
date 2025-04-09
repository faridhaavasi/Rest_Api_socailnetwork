from django.urls import path , include

app_name = 'post'
urlpatterns = [
    path('api/v1/', include('apps.posts.api.v1.urls'), name='posts-v1'),

]