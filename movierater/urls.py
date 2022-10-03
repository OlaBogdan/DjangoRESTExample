from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from api import urls as api_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('auth/', obtain_auth_token)
]
