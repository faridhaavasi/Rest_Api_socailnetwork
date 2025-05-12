from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated  
from rest_framework.response import Response
from rest_framework import status
from apps.account.models import FollowerModel
from apps.account.models import AccountModel
class FollowUserApiView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, user_id):
        try:
            user = request.user
            follow_user = AccountModel.objects.get(id=user_id)
            if user == follow_user.user:
                return Response({"message": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            FollowerModel.objects.create(user=follow_user.user, follower=user)
            return Response({"message": "Followed successfully."}, status=status.HTTP_201_CREATED)
        except AccountModel.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)