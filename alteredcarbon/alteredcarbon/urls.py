"""alteredcarbon URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api import views
from api.views import ErrorLogViewSet, UpdateCheckViewSet, FirmwareViewSet

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register('error_reporting', ErrorLogViewSet, basename='log_error')
router.register('check_update', UpdateCheckViewSet, basename='check_update')
router.register('firmware', FirmwareViewSet, basename='firmware')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index, name='index'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += router.urls
