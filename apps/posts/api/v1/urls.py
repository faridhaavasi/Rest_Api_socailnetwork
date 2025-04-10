from django.urls import path
from apps.posts.api.v1.views.post_views import (
    PostCreateViewApi,
    PostListAllViewApi,
    PostListPublishedViewApi,
    PostDetailViewApi,
    PostDeleteViewApi,
    PostUpdateViewApi
)

app_name = 'posts_v1'
urlpatterns = [
    path('posts/create/', PostCreateViewApi.as_view(), name='create_post'), # Create a new post
    path('posts/', PostListAllViewApi.as_view(), name='list_all_posts'), # List all posts
    path('posts/published/', PostListPublishedViewApi.as_view(), name='list_published_posts'), # List pubilished posts
    path('posts/<int:pk>/', PostDetailViewApi.as_view(), name='post_detail'), # detail post 
    path('posts/<int:pk>/update/', PostUpdateViewApi.as_view(), name='update_post'), # update post
    path('posts/<int:pk>/delete/', PostDeleteViewApi.as_view(), name='delete_post'), # delete post
]