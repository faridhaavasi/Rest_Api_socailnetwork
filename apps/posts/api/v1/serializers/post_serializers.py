from rest_framework import serializers
from apps.posts.models import Post, Comment


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
                'published_at', 'comments'
                ]

             
          
        
class InputCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'replay', 'author', 'content']
        read_only_fields = ['author']
        extra_kwargs = {
            'post': {'required': True},
            'replay': {'required': False},
            'author': {'required': False},
            'content': {'required': True},
        }

class OutputCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'replay', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'post': {'required': True},
            'replay': {'required': False},
            'author': {'required': False},
            'content': {'required': True},
        }

class ReplayCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['replay']
        read_only_fields = ['replay']
        extra_kwargs = {
            'replay': {'required': True},
        }
        