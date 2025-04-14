from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime
from django.contrib.auth import get_user_model

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
