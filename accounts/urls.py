from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter



urlpatterns = [
    
    path('user/', views.CreateUserSK.as_view(), name="create_user"),
    path('user/key/', views.KeyValidator.as_view(), name="key_validator"),

]
   
