from accounts.permissions import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from .helpers.generators import generate_password
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, logout
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework import generics
from rest_framework.decorators import action
from djoser.views import UserViewSet
from rest_framework.views import APIView
from .models import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Permission, Group
from .emails import user_sk_mail
import string
import random
from django.db.models import Q
import requests
import os



def generate_sk():
    
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(20))

    return f"sk_{random_string}"


 
 
User = get_user_model()


def get_query():
    
    """returns query to be used to in the permissions view"""
    
    exclude_words = [ "activationotp", "activitylog", "moduleaccess", "logentry","group", "permission", "contenttype", "userinbox", "validationotp", "session", "blacklistedtoken", "outstandingtoken", "cart", ]
    
    query = Q()
    for word in exclude_words:
        query |= Q(codename__icontains=word)
        
    return query
    
   



class CustomUserViewSet(UserViewSet):
    queryset = User.objects.filter(is_deleted=False)
    
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(role="user")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("current_password")
        
        if check_password(password, instance.password):
            
            self.perform_destroy(instance)
            ActivityLog.objects.create(
                user=instance,
                action = f"Deleted account"
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        elif request.user.role == "admin" and check_password(password, request.user.password):
            self.perform_destroy(instance)
            ActivityLog.objects.create(
                user=request.user,
                action = f"Deleted account with ID {instance.id}"
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        # elif password=="google" and request.user.provider=="google":
        #     self.perform_destroy(instance)
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise AuthenticationFailed(detail={"message":"incorrect password"})

            
            



@swagger_auto_schema(method='post', request_body=LoginSerializer())
@api_view([ 'POST'])
def user_login(request):
    
    """Allows users to log in to the platform. Sends the jwt refresh and access tokens. Check settings for token life time."""
    
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = authenticate(request, email = data['email'], password = data['password'], is_deleted=False)

            if user:
                if user.is_active==True:
                
                    try:
                        
                        refresh = RefreshToken.for_user(user)

                        user_detail = {}
                        user_detail['id']   = user.id
                        user_detail['first_name'] = user.first_name
                        user_detail['last_name'] = user.last_name
                        user_detail['email'] = user.email
                        user_detail['phone'] = user.phone
                        user_detail['role'] = user.role
                        user_detail['is_admin'] = user.is_admin
                        user_detail['is_superuser'] = user.is_superuser
                        user_detail['access'] = str(refresh.access_token)
                        user_detail['refresh'] = str(refresh)
                        user_logged_in.send(sender=user.__class__,
                                            request=request, user=user)

                        if user.role == 'admin':
                            user_detail["modules"] = user.module_access
                            
                        data = {
    
                        "message":"success",
                        'data' : user_detail,
                        }
             
                        return Response(data, status=status.HTTP_200_OK)
                    

                    except Exception as e:
                        raise e
                
                else:
                    data = {
                    
                    'error': 'This account has not been activated'
                    }
                return Response(data, status=status.HTTP_403_FORBIDDEN)

            else:
                data = {
                    
                    'error': 'Please provide a valid email and a password'
                    }
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
                data = {
                    
                    'error': serializer.errors
                    }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            
@swagger_auto_schema(method="post",request_body=LogoutSerializer())
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Log out a user by blacklisting their refresh token then making use of django's internal logout function to flush out their session and completely log them out.

    Returns:
        Json response with message of success and status code of 204.
    """
    
    serializer = LogoutSerializer(data=request.data)
    
    serializer.is_valid(raise_exception=True)
    
    try:
        token = RefreshToken(token=serializer.validated_data["refresh_token"])
        token.blacklist()
        user=request.user
        user_logged_out.send(sender=user.__class__,
                                        request=request, user=user)
        logout(request)
        
        return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)
    except TokenError:
        return Response({"message": "failed", "error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="patch",request_body=FirebaseSerializer())
@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_firebase_token(request):
    """Update the FCM token for a logged in use to enable push notifications

    Returns:
        Json response with message of success and status code of 200.
    """
    
    serializer = FirebaseSerializer(data=request.data)
    
    serializer.is_valid(raise_exception=True)
    
    fcm_token = serializer.validated_data.get("fcm_token")

    request.user.fcm_token = fcm_token
    request.user.save()
        
    return Response({"message": "success"}, status=status.HTTP_200_OK)
    



@swagger_auto_schema(methods=['POST'],  request_body=NewOtpSerializer())
@api_view(['POST'])
def reset_otp(request):
    if request.method == 'POST':
        serializer = NewOtpSerializer(data = request.data)
        if serializer.is_valid():
            data = serializer.get_new_otp()
            
            return Response(data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        
            
@swagger_auto_schema(methods=['POST'], request_body=OTPVerifySerializer())
@api_view(['POST'])
def otp_verification(request):
    
    """Api view for verifying OTPs """

    if request.method == 'POST':

        serializer = OTPVerifySerializer(data = request.data)

        if serializer.is_valid():
            data = serializer.verify_otp(request)
            
            return Response(data, status=status.HTTP_200_OK)
        else:
  
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        



class CreateUserSK(APIView):

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user.sk = generate_sk()
            user.save()
            data = {
                "email": user.email,
                "sk": user.sk,
            }
            # user_sk_mail(user)
            return Response(data, status=200)
        
        else:
            user = User.objects.create(
                email=email,
                sk = generate_sk(),
                role='user'

            )
            data = {
                "email": user.email,
                "sk": user.sk,
            }

            return Response(data, status=200)



class KeyValidator(APIView):

    def post(self, request):

        serializer = request.data
        if "key" in serializer:
            key = serializer["key"]
            if User.objects.filter(sk=key).exists():
                user = User.objects.get(sk=key)
                data = {
                    "email": user.email,

                }
                return Response(data, status=200)
            else:
                return Response(status=401)
            
        else:
            return Response(status=403)
            
        


        