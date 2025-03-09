from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.api.v1.serializers.register_signup_serializers import (
    StepSetEmailRegisterSerializer,
)
from django.conf import settings
from apps.users.models import User
from apps.authentication.utils import EmailMessage, EmailSendThread


class SeteEailApiView(GenericAPIView):
    serializer_class = StepSetEmailRegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user, vlaue = User.objects.get_or_create(email=email)
            user.is_active = False
            user.save()
            token = RefreshToken.for_user(user).access_token

            email_obj = EmailMessage(
                subject='Confirm your email',
                body=f' click in link: {str(token)}',
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )
            
            EmailSendThread(email_obj=email_obj).start()
            
            print(token)
            return Response({'message': 'Registration successful! Please check your email to confirm your account.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
