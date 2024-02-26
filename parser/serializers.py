from .models import *
from rest_framework import serializers





class B64_TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = B64_Table
        fields = '__all__'



class Content(serializers.Serializer):

    image = serializers.ImageField(max_length=None, use_url=True, required=True)