from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from apps.posts.models import Comment, Replay
from apps.posts.api.v1.serializers.comment_serializer import (
    InputCommentSerializer,
    OutputCommentSerializer,
)