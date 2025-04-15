from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime
from django.contrib.auth import get_user_model
from apps.posts.models import Post
User = get_user_model()

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def create_user():
    user = User.objects.create_user(
        email="admin@admin.com", password="a/@1234567", is_verify=True
    )
    return user

@pytest.mark.django_db
class TestPostApi:
    def test__create_post(self, api_client, create_user):
        api_client.force_authenticate(user=create_user)
        url = reverse("posts_v1:create_post")
        data = {
            "title": "Test Post",
            "content": "This is a test post.",
            "author": create_user.id,
            "is_published": True,

            
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == 201

    def test__list_post(self, api_client, create_user):
        api_client.force_authenticate(user=create_user)
        url = reverse("posts_v1:list_all_posts")
        response = api_client.get(url, format="json")
        assert response.status_code == 200
    
    def test__list_published_post(self, api_client, create_user):
        api_client.force_authenticate(user=create_user)
        url = reverse("posts_v1:list_published_posts")
        response = api_client.get(url, format="json")
        assert response.status_code == 200


    def test__detail_post(self, api_client, create_user):
        api_client.force_authenticate(user=create_user)
        
        post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=create_user,
            is_published=True
        )
        url = reverse("posts_v1:post_detail", args=[post.id])
        response = api_client.get(url, format="json")
        assert response.status_code == 200
        assert response.data["id"] == post.id
        assert response.data["title"] == post.title
        assert response.data["content"] == post.content
        assert response.data["author"] == post.author.id

    def test__update_post(self, api_client, create_user):
        api_client.force_authenticate(user=create_user)
        
        post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=create_user,
            is_published=True
        )
        url = reverse("posts_v1:update_post", args=[post.id])
        data = {
            "title": "Updated Test Post",
            "content": "This is an updated test post.",
            "author": create_user.id,
            "is_published": True,
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == 200
        post.refresh_from_db()
        assert post.title == "Updated Test Post"
        assert post.content == "This is an updated test post."
        assert post.author == create_user

    def test__delete_post(self, api_client, create_user):
        api_client.force_authenticate(user=create_user)
        
        post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=create_user,
            is_published=True
        )
        url = reverse("posts_v1:delete_post", args=[post.id])
        response = api_client.delete(url, format="json")
        assert response.status_code == 204
        assert Post.objects.filter(id=post.id).count() == 0

  