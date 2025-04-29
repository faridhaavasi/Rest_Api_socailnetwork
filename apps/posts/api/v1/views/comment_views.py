from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.posts.api.v1.serializers.post_serializers import InputCommentSerializer, OutputCommentSerializer
from apps.posts.models import Comment
from apps.posts.permissions import IsAuthorOnly
from django.contrib.auth import get_user_model


user = get_user_model()  # Custom user model global variable

class CommentViewSet(viewsets.ModelViewSet):
    """
    API view to create, retrieve, update, and delete comments.
    """
    serializer_class = InputCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Create a new comment.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            post = serializer.validated_data.get('post')
            content = serializer.validated_data.get('content')
            replay = serializer.validated_data.get('replay')

            Comment.objects.create(
                post=post,
                content=content,
                author=user,
                replay=replay
            )
            return Response({"message": "Comment created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
