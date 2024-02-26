from django.urls import path, include
from .views import *








urlpatterns = [

    path('content/', Converter.as_view()),
    path('<str:id>/', ViewContent.as_view()),
   
]
