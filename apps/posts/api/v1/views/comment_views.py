from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.posts.models import Comment, Post
from apps.posts.api.v1.serializers.comment_serializer import InputCommentSerializer, OutputCommentSerializer
from django.shortcuts import get_object_or_404


class CommentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH),
        ],
        responses=OutputCommentSerializer(many=True)
    )
    def list(self, request, post_id=None):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = OutputCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH),
        ],
        request=InputCommentSerializer,
        responses=OutputCommentSerializer
    )
    def create(self, request, post_id=None):
        serializer = InputCommentSerializer(data=request.data)
        if serializer.is_valid():
            is_replay = serializer.validated_data.get('is_replay', False)

            if is_replay:
                comment_replay = get_object_or_404(Comment, id=serializer.validated_data.get('replay'))
                serializer.save(
                    post=comment_replay.post,
                    author=request.user,
                    is_replay=True,
                    replay=comment_replay
                )
            else:
                post_instance = get_object_or_404(Post, id=post_id)
                serializer.save(
                    post=post_instance,
                    author=request.user,
                    is_replay=False
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
