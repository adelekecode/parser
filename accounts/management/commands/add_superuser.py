from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create Dummy Box locations'


    def handle(self, *args, **options):
        
        email = input("Email:\n>")
        phone = input("Phone:\n>")
        password = input("Password:\n>")
        
        
        User.objects.create_superuser(email=email, password=password, phone=phone)
        
        self.stdout.write(self.style.SUCCESS("Successfully added superuser"))