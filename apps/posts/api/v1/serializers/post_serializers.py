from rest_framework import serializers
from apps.posts.models import Post


class InputPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'image', 'content', 'author', 'is_published']


class OutputPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 
                'image', 'content', 
                'author', 'created_at',
                'updated_at', 'is_published',
                'published_at'

               ] 
          
        
