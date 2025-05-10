from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.posts.api.v1.views.comment_views import CommentViewSet
from apps.posts.api.v1.views.post_views import (
    PostCreateViewApi,
    PostListAllViewApi,
    PostListPublishedViewApi,
    PostDetailViewApi,
    PostDeleteViewApi,
    PostUpdateViewApi,
)
from apps.posts.api.v1.views.like_views import LikeViewSet

app_name = 'posts_v1'

router = DefaultRouter()
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='post-comments'
)
router.register(r'likes', LikeViewSet, basename='likes')

urlpatterns = [
    # Post Views
    path('posts/create/', PostCreateViewApi.as_view(), name='create_post'),
    path('posts/', PostListAllViewApi.as_view(), name='list_all_posts'),
    path('posts/published/', PostListPublishedViewApi.as_view(), name='list_published_posts'),
    path('posts/<int:pk>/', PostDetailViewApi.as_view(), name='post_detail'),
    path('posts/<int:pk>/update/', PostUpdateViewApi.as_view(), name='update_post'),
    path('posts/<int:pk>/delete/', PostDeleteViewApi.as_view(), name='delete_post'),

    # Comment routes
    path('', include(router.urls)),
]
