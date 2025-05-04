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

# ایجاد Router برای ViewSet کامنت‌ها
router = DefaultRouter()
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='post-comments')

# تعریف آدرس‌ها
app_name = 'posts_v1'

urlpatterns = [
    # Post Views
    path('posts/create/', PostCreateViewApi.as_view(), name='create_post'),               # ایجاد پست جدید
    path('posts/', PostListAllViewApi.as_view(), name='list_all_posts'),                  # لیست همه پست‌ها
    path('posts/published/', PostListPublishedViewApi.as_view(), name='list_published_posts'),  # پست‌های منتشر شده
    path('posts/<int:pk>/', PostDetailViewApi.as_view(), name='post_detail'),             # جزییات یک پست خاص
    path('posts/<int:pk>/update/', PostUpdateViewApi.as_view(), name='update_post'),      # ویرایش پست
    path('posts/<int:pk>/delete/', PostDeleteViewApi.as_view(), name='delete_post'),      # حذف پست

    # Comment ViewSet via router
    path('', include(router.urls)),  # شامل URL‌های خودکار ViewSet کامنت‌ها
]
