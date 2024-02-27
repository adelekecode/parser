from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions, authentication # new

from drf_yasg.views import get_schema_view # new
from drf_yasg import openapi 

schema_view = get_schema_view(
    openapi.Info(
        title="Parser",
        default_version="v1.1",
        description="adelekecode",
        terms_of_service="",
        contact=openapi.Contact(email="oluwafemiadeleke13@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(authentication.BasicAuthentication,)
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('v1/', include('accounts.urls')),
    path('v1/', include('parser.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
