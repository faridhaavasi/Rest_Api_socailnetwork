from rest_framework import serializers
from apps.users.models import User

class StepSetEmailRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):  
        is_exists_email = User.objects.filter(email=value).exists()
        if is_exists_email:
            raise serializers.ValidationError('This email exists')
        return value  


