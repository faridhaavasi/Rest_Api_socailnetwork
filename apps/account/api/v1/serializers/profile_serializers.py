from rest_framework import serializers
from apps.account.models import AccountModel

class GetProfileSerializer(serializers.ModelSerializer):
    is_following = serializers.BooleanField(source='is_following', read_only=True)
    followers_count = serializers.IntegerField(source='followers_count', read_only=True)
    following_count = serializers.IntegerField(source='following_count', read_only=True)
    class Meta:
        model = AccountModel
        fields = '__all__'

        