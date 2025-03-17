from rest_framework import serializers
from apps.account.models import AccountModel

class GetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = '__all__'

        