
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import (DjangoModelPermissions)
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework import exceptions
from django.contrib.auth import get_user_model
# from accounts.models import User

User = get_user_model()




class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        
        


class CustomBasePermissions(BasePermission):
    
    
    def __init__(self):
        self.model = None
    
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    
    authenticated_users_only = True
    
    def get_required_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }


        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)
        
        return [perm % kwargs for perm in self.perms_map[method]]
    
    
    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
           not request.user.is_authenticated and self.authenticated_users_only):
            return False

        perms = self.get_required_permissions(request.method, self.model)

        return request.user.has_perms(perms)
    
    
class UserTablePermissions(CustomBasePermissions):
    
    def __init__(self):
        self.model = User
    
        


#put custom permissions here


class IsAdmin(BasePermission):
   
    def has_permission(self, request, view):

        if isinstance(request.user, AnonymousUser):
            raise AuthenticationFailed(detail="Authentication credentials were not provided")
        
        if request.user.role == "admin":
            return True
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided")




def AuthHandler(request):
        
    if 'Authorization' in request.headers:

        auth_header = request.headers['Authorization']
        
        token = auth_header.split(' ')[1]

        if User.objects.filter(sk=token).exists():

            return User.objects.get(sk=token)
        
        else:
            raise PermissionDenied(detail="Unauthorized access -- Incorrect or invalid auth key")
    else:
        raise PermissionDenied(detail="Unauthorized access -- Auth key not provided")
