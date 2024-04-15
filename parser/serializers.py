from .models import *
from rest_framework import serializers





class EncodingSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = ImageEncoding
        fields = '__all__'



class Content(serializers.Serializer):

    file = serializers.FileField(max_length=None, use_url=True, required=True)