from django.shortcuts import render
from accounts.permissions import *
# Create your views here.
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

        image = serializer.validated_data['image']
        b64 = base64.b64encode(image.read()).decode('utf-8')

        id = ImageEncoding.objects.create(
            b64=b64,
            user=user
        )
        if envs == "dev":
            url = "http://127.0.0.1:8000"
        

        data = {
            "status": "accepted",
            "code": 200,
            "url": f"{url}/v1/{id.created_at}/{id.unique_id}"

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
        
        image = b64.b64
        img_bytes = base64.b64decode(image)

        return HttpResponse(img_bytes, content_type="image/jpeg")

        









