from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.account.models import AccountModel
from apps.account.api.v1.serializers.profile_serializers import GetProfileSerializer

class GetProfileView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        profile = AccountModel.objects.get(user=request.user)
        serializer = GetProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
