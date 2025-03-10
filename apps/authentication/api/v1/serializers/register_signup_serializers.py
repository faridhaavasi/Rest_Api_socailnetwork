from rest_framework import serializers
from apps.users.models import User

class StepSetEmailRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):  
        is_exists_email = User.objects.filter(email=value).exists()
        if is_exists_email:
            raise serializers.ValidationError('This email exists')
        return value  
    

class StepSetPasswordRegisterSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Passwords do not match')
        return data
    
    def validate_password(self, value):
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError('Password must contain at least one digit')
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError('Password must contain at least one letter')
        return value


class RestorePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email does not exist')
        return value
    
    
class RestorePasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Passwords do not match')
        return data
    
    def validate_password(self, value):
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError('Password must contain at least one digit')
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError('Password must contain at least one letter')
        return value    