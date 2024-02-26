from django.db import models
import uuid
from .helpers import generate_sk

# Create your models here.









class User(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    email = models.EmailField(max_length=100, unique=True, null=True)
    sk = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)



    def __str__(self) -> str:
        return self.username
    

    def save(self, *args, **kwargs):
        self.sk = generate_sk()

        return super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.is_deleted = True
        return super().delete(*args, **kwargs)
    

    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'



