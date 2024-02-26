from django.urls import path, include
from .views import *








urlpatterns = [

    path('generate/auth_key/', CreateSecretKey.as_view(), name="generate_auth_key"),
   
]
