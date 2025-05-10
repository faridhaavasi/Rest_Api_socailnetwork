from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from apps.posts.models import Like, Post

class LikeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path=r'(?P<post_id>\d+)/like')
    def like(self, request, post_id=None):
        user = request.user
        post = get_object_or_404(Post, id=post_id)

        if Like.objects.filter(user=user, post=post).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(user=user, post=post)
        return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path=r'(?P<post_id>\d+)/unlike')
    def unlike(self, request, post_id=None):
        user = request.user
        like = Like.objects.filter(user=user, post_id=post_id).first()

        if not like:
            return Response({"error": "Like not found."}, status=status.HTTP_404_NOT_FOUND)

        like.delete()
        return Response({"message": "Like removed successfully."}, status=status.HTTP_204_NO_CONTENT)
