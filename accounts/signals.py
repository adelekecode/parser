import random
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from config import settings
from djoser.signals import user_registered, user_activated

from .models import ActivationOtp
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
import json
import os
import  requests


User = get_user_model()
site_name = ""


def generate_otp(n):
    return "".join([str(random.choice(range(10))) for _ in range(n)])

    

@receiver(post_save, sender=User)
def user_mail(sender, instance, created, **kwargs):

    if created:


        return