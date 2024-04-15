from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
import uuid 
from django.forms import model_to_dict
from django.core.exceptions import ValidationError
import hashlib
from django.utils.text import slugify
from .helpers import unique_id
# Create your models here.





class ImageEncoding(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    unique_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="encoded_images")
    b64 = models.TextField()
    file_type = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> Any:
        self.unique_id = unique_id()
        return super().save(*args, **kwargs)


    def __str__(self) -> str:
        return f"{self.unique_id}"
    


