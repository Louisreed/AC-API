"""alteredcarbon URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from api import views
from api.views import logError, checkUpdateAvailable, getFirmware

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register('error_reporting', logError, basename='logError')
router.register('check_update', checkUpdateAvailable, basename='check_update')
router.register('firmware', getFirmware, basename='firmware')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index, name='index'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
