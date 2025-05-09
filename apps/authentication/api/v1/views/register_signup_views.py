import uuid
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from apps.authentication.api.v1.serializers.register_signup_serializers import (
    StepSetEmailRegisterSerializer,
    StepSetPasswordRegisterSerializer,
    RestorePasswordSerializer,
    RestorePasswordConfirmSerializer
)
from django.conf import settings
from apps.users.models import User
from apps.authentication.models import TokenModel
from apps.authentication.utils import EmailMessage, EmailSendThread
from apps.account.models import AccountModel

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
            value_token = uuid.uuid4()
            TokenModel.objects.create(token=token, value=str(value_token))
            url_confirm = f"{settings.FRONTEND_URL}{reverse('authentication:confirm_email', args=[str(value_token)])}"

            email_obj = EmailMessage(
                subject='Confirm your email',
                body= url_confirm,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )
            
            EmailSendThread(email_obj=email_obj).start()
            
            print(token)
            return Response({'message': 'Registration successful! Please check your email to confirm your account.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmEmailApiView(GenericAPIView):
    def get(self, request, value_token):
        try:
            obj_token = TokenModel.objects.get(value=value_token)
            token = obj_token.token
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # get user id from token
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.is_verify = True
            user.save()
            AccountModel.objects.create(user=user)

            return Response({'message': 'Email confirmed successfully!', 'access_token':str(access_token)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordApiView(GenericAPIView):
    serializer_class = StepSetPasswordRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                token = serializer.validated_data['token']
                access_token = AccessToken(token)  #  decode token
                user_id = access_token['user_id']  # get user id from token

                user = User.objects.get(id=user_id)  #  find user by id 
                password = serializer.validated_data['password']

                user.set_password(password)
                user.save()

                return Response({'message': 'Password set successfully!'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RestorePasswordApiView(GenericAPIView):
    serializer_class = RestorePasswordSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token = RefreshToken.for_user(user).access_token
            value = uuid.uuid4()
            TokenModel.objects.create(token=token, value=value)
            url_restore_password = f"{settings.FRONTEND_URL}{reverse('authentication:restore_password_confirm', args=[str(value)])}"

            email_obj = EmailMessage(
                subject='Restore password',
                body=f"{url_restore_password}",
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )
            
            EmailSendThread(email_obj=email_obj).start()
            
            return Response({'message': 'Email sent successfully!'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class RestorePasswordConfirmApiView(GenericAPIView):
    serializer_class = RestorePasswordConfirmSerializer
    def put(self, request, value):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                token_object = TokenModel.objects.get(value=value)
                token = token_object.token
                access_token = AccessToken(token)  #  decode token
                user_id = access_token['user_id']  # get user id from token

                user = User.objects.get(id=user_id)  #  find user by id 
                password = serializer.validated_data['password']

                user.set_password(password)
                user.save()

                return Response({'message': 'Password set successfully!'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)