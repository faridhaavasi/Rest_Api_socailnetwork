from rest_framework import serializers
from apps.posts.models import Comment, Replay

class InputCommentSerializer(serializers.Serializer):
    content = serializers.CharField()
    reply_content = serializers.CharField(required=False, allow_blank=True)

class ReplaySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Replay
        fields = ['id', 'content', 'author', 'created_at']

class OutputCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    replies = ReplaySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'replies']


