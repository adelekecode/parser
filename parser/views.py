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







class Converter(APIView):

    def post(self, request):


        serializer = Content(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = serializer.validated_data['image']
        b64 = base64.b64encode(image.read()).decode('utf-8')

        id = B64_Table.objects.create(b64=b64)

        data = {
            "status": "accepted",
            "url": f"http://127.0.0.1:8000/v1/{id.unique_id}"

        }

        return Response(data, status=200)
    




class ViewContent(APIView):

    def get(self, request, id):

        try:
            b64 = B64_Table.objects.get(unique_id=id)
        except B64_Table.DoesNotExist:
            return Response({"status": "not found"}, status=404)
        
        image = b64.b64
        img_bytes = base64.b64decode(image)

        return HttpResponse(img_bytes, content_type="image/jpeg")

        









