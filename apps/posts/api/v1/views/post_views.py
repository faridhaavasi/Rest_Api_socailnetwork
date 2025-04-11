from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.posts.permissions import IsAuthorOnly
from apps.posts.models import Post
from apps.posts.api.v1.serializers.post_serializers import InputPostSerializer, OutputPostSerializer
from django.contrib.auth import get_user_model

user = get_user_model()  # Custom user model global variable


class PostCreateViewApi(GenericAPIView):
    """
    API view to create a new post.
    """
    serializer_class = InputPostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create a new post.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content')
            image = serializer.validated_data.get('image')
            is_published = serializer.validated_data.get('is_published')

            Post.objects.create(
                title=title,
                content=content,
                image=image,
                author=user,
                is_published=is_published
            )
            return Response({"message": "Post created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class PostListAllViewApi(GenericAPIView):
    """
    API view to list all posts.
    """
    serializer_class = OutputPostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOnly]

    def get(self, request):
        """
        List all posts.
        """
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostListPublishedViewApi(GenericAPIView):
    """
    API view to list published posts.
    """
    serializer_class = OutputPostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOnly]

    def get(self, request):
        """
        List published posts.
        """
        posts = Post.objects.posts_published()
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDetailViewApi(GenericAPIView):
    """
    API view to retrieve, update, or delete a post.
    """
    serializer_class = OutputPostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOnly]

    def get(self, request,pk):
        """
        Retrieve a post by ID.
        """
        try:
            post = Post.objects.get(id=pk)
            serializer = self.serializer_class(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

class PostUpdateViewApi(GenericAPIView):
    """
    API view to update a post.
    """
    serializer_class = InputPostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOnly]

    def put(self, request, pk):
        """
        Update a post by ID.
        """
        try:
            post = Post.objects.get(id=pk)
            serializer = self.serializer_class(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

class PostDeleteViewApi(GenericAPIView):
    """
        API view to delete a post.
    """
    permission_classes = [IsAuthenticated, IsAuthorOnly]
    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            post.delete()
            return Response({"messagr": "post deleted"}, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
