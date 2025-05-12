from rest_framework import serializers
from apps.posts.models import Post
from apps.posts.api.v1.serializers.comment_serializer import OutputCommentSerializer


class InputPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Post
        fields = ['title', 'slug', 'image', 'content', 'author', 'is_published']
        read_only_fields = ['author']
        extra_kwargs = {
            'title': {'required': True},
            'slug': {'required': False},
            'image': {'required': False},
            'content': {'required': True},
            'is_published': {'required': False},
        }


class OutputPostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    def get_likes(self, obj):
        return obj.likes.count()
    comments = serializers.SerializerMethodField()
    def get_comments(self, obj):
        comments = obj.comments.all()
        return OutputCommentSerializer(comments, many=True).data
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 
                'image', 'content', 
                'author', 'created_at',
                'updated_at', 'is_published',
                'published_at', 'comments',
                'likes'
                ]

             
