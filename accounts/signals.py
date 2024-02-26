import random
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from config import settings
from djoser.signals import user_registered, user_activated
from .mail import *
from .helpers import *

from django.utils import timezone
from .models import *





@receiver(post_save, sender=User)
def user_mail(sender, instance, created, **kwargs):

    if created:

        user = instance
        user_sk_mail(user)

        return
