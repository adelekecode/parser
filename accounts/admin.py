from rest_framework_simplejwt.token_blacklist import models, admin


class CustomOutstandingTokenAdmin(admin.OutstandingTokenAdmin):
    
    def has_delete_permission(self, *args, **kwargs):
        return True

from django.contrib import admin
from django.contrib.auth.models import Permission



    
    
admin.site.unregister(models.OutstandingToken)
admin.site.register(models.OutstandingToken, CustomOutstandingTokenAdmin)
