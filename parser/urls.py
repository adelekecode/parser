from django.urls import path, include
from .views import *








urlpatterns = [

    path('content/', ImageParser.as_view()),
    path('<str:cr_at>/<str:id>/', ViewContent.as_view()),
   
]
