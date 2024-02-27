from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.forms import model_to_dict
from .managers import UserManager
from .helpers.generators import generate_sk
import uuid
import random


class User(AbstractBaseUser, PermissionsMixin):
  
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )   
    
    
    
    
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
  
    role          = models.CharField(_('role'), max_length = 255, choices=ROLE_CHOICES, null=True)
    email         = models.EmailField(_('email'), unique=True)
    sk            = models.CharField(_('sk'), max_length=255, null=True)
    
    is_staff      = models.BooleanField(_('staff'), default=False)
    is_admin      = models.BooleanField(_('admin'), default= False)
    is_active     = models.BooleanField(_('active'), default=True)
    is_deleted    = models.BooleanField(_('deleted'), default=False)
    date_joined   = models.DateTimeField(_('date joined'), auto_now_add=True)

    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['id', 'role',]
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.email} -- {self.role}"
    
    
    def save(self, *args, **kwargs):
        self.sk = generate_sk()

        return super().save(*args, **kwargs)
 
    
    
    def delete(self):
        
        self.is_deleted = True
        self.email = f"{random.randint(0,100000)}-deleted-{self.email}"
        self.phone = f"{self.phone}-deleted-{random.randint(0,100000)}"
        self.save()
        
        return 
        
    def delete_permanently(self):
        
        super().delete()
        
        return 
        
        
   
    
        
        
class ActivationOtp(models.Model):
 

    user  =models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expiry_date = models.DateTimeField()
    
    
    def is_valid(self):
        
        return bool(self.expiry_date > timezone.now())



class ActivityLog(models.Model):
    
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    
    def delete(self):
        self.is_deleted = True
        self.save()
        
        
    def delete_permanently(self):
        super().delete()
        
        
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.action}"
    
    
    