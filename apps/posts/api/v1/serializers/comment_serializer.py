from rest_framework import serializers
from apps.posts.models import Comment




        
class InputCommentSerializer(serializers.ModelSerializer):
    is_replay = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = Comment
        fields = ['post', 'replay', 'author', 'content']
        read_only_fields = ['author']
        extra_kwargs = {
            'post': {'required': True},
            'replay': {'required': False},
            'author': {'required': False},
            'content': {'required': True},
            'is_replay': {'required': False},
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
        