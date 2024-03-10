### global cache config 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page




class GlobalCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method == 'GET' and response.status_code == 200:

            response['Cache-Control'] = 'max-age=1800'  # Cache for 30 minutes

        return response
