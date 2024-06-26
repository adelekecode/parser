from django.shortcuts import render
from accounts.permissions import *
from django.http import FileResponse
from django.http import HttpResponse
import base64
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, logout
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView , RetrieveUpdateAPIView
from rest_framework.decorators import action
from djoser.views import UserViewSet
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import requests
import os
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


url = os.getenv("base_url")
envs = os.getenv("ENVIRONMENT")


class Welcome(APIView):

    def get(self, request):

        data = {
            "status": "all systems go!",
            "code": 200,
            "message": "welcome to the parser api"
        }

        return Response(data, status=200)


class ImageParser(APIView):


    def post(self, request):

        user = AuthHandler(request)

        serializer = Content(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data['file']

        if 'file_type' in serializer.validated_data:
            file_type = serializer.validated_data['file_type']

        else:
            file_type = file.content_type

        b64 = base64.b64encode(file.read()).decode('utf-8')


        id = ImageEncoding.objects.create(
            b64=b64,
            user=user,
            file_type=file_type

        )


        if envs == "dev":
            url = "http://127.0.0.1:8000"

        else:
            url = os.getenv("base_url")
        

        data = {
            "status": "accepted",
            "code": 200,
            "url": f"{url}/v1/{id.created_at}/{id.unique_id}",
            "file_type": id.file_type,
            "created_at": str(id.created_at),
            "unique_id": str(id.unique_id)

        }

        return Response(data, status=200)
    

@method_decorator(cache_page(30*60), name='dispatch')
class ViewContent(APIView):

    def get(self, request, cr_at, id):

        try:
            b64 = ImageEncoding.objects.get(unique_id=id)
        except ImageEncoding.DoesNotExist:
            return Response({"status": "not found"}, status=404)
        
        if cr_at != str(b64.created_at):
            return Response({"status": "wrong timeframe"}, status=404)
        

        file_bytes = base64.b64decode(b64.b64)
        if b64.file_type == None:
            return HttpResponse(file_bytes, content_type="image/jpeg")
        
        elif b64.file_type == "":
            return HttpResponse(file_bytes, content_type="image/jpeg")
        
        else:
       
            return HttpResponse(file_bytes, content_type=str(b64.file_type))

        

class GetImages(APIView):

    def get(self, request):

        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"status": "user not found"}, status=404)

        images = ImageEncoding.objects.filter(user=user).order_by("-created_at")

        data = []
        if envs == "dev":
            url = "http://127.0.0.1:8000"

        else:
            url = os.getenv("base_url")

        for image in images:
            obj = {
                "url": f"{url}/v1/{image.created_at}/{image.unique_id}",
                "created_at": str(image.created_at),
                "unique_id": str(image.unique_id)
            }

            data.append(obj)

        return Response(data, status=200)



