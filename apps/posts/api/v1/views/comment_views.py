from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.posts.models import Post, Comment, Replay
from apps.posts.api.v1.serializers.comment_serializer import (
    InputCommentSerializer,
    OutputCommentSerializer,
)

class CommentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name="post_id", type=int, location=OpenApiParameter.PATH)
        ],
        responses=OutputCommentSerializer(many=True),
    )
    def list(self, request, post_id=None):
        comments = Comment.objects.filter(post_id=post_id).prefetch_related("replies", "author")
        serializer = OutputCommentSerializer(comments, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="post_id", type=int, location=OpenApiParameter.PATH)
        ],
        request=InputCommentSerializer,
        responses=OutputCommentSerializer,
    )
    def create(self, request, post_id=None):
        serializer = InputCommentSerializer(data=request.data)
        if serializer.is_valid():
            post = get_object_or_404(Post, id=post_id)

            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=serializer.validated_data["content"]
            )

            if serializer.validated_data.get("reply_content"):
                Replay.objects.create(
                    comment=comment,
                    author=request.user,
                    content=serializer.validated_data["reply_content"]
                )

            output_serializer = OutputCommentSerializer(comment)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=["get"], url_path="replies")
    def list_replies(self, request, post_id=None, pk=None):
        """
        List all replies for a specific comment.
        """
        comment = get_object_or_404(Comment, pk=pk, post_id=post_id)
        replies = comment.replies.all()  # reverse relation
        serializer = OutputCommentSerializer(replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get", "post"], url_path="replies")
    def handle_replies(self, request, post_id=None, pk=None):
        comment = get_object_or_404(Comment, pk=pk, post_id=post_id)

        if request.method == 'GET':
            replies = comment.replies.all()
            serializer = OutputCommentSerializer(replies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            serializer = InputCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                post=comment.post,
                author=request.user,
                is_replay=True,
                reply=comment
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
