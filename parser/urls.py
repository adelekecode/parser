from django.urls import path, include
from .views import *








urlpatterns = [

    path('upload/content/', ImageParser.as_view()),
    path('<str:cr_at>/<str:id>/', ViewContent.as_view()),
    path('images/', GetImages.as_view()),
   
]
