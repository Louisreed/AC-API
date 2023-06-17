# import os
# from django.shortcuts import render
# from rest_framework.decorators import api_view
from .serializers import ErrorLogSerializer, UpdateCheckSerializer, FirmwareSerializer, UserSerializer, GroupSerializer
from django.contrib.auth.models import User, Group
from .models import ErrorLog, UpdateCheck, Firmware
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
import re
from .serializers import UserSerializer, GroupSerializer, ErrorLogSerializer, UpdateCheckSerializer, FirmwareSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ErrorLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows error logs to be viewed or edited.
    """
    queryset = ErrorLog.objects.all()
    serializer_class = ErrorLogSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdateCheckViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows updates to be viewed or edited.
    """
    queryset = UpdateCheck.objects.all()
    serializer_class = UpdateCheckSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
    def retrieve(self, request, pk=None):
        update_check = self.get_object()
        version = update_check.version
        checked_date = update_check.checked_date
        
        if float(settings.APP_VERSION) > float(version):
            data = {'version': version, 'checked_date': checked_date, 'status': 'update_available'}
        else:    
            data = {'version': version, 'checked_date': checked_date, 'status': 'system_upto_date'}
        
        return Response(data)


    
    # def retrieve(self, request, pk=None):
    #     update_check = self.get_object()
    #     serializer = UpdateCheckSerializer(update_check)

    #     version = update_check.version
    #     print('Version:', version)
        
    #     # version = str(version).replace('_', '.')
    #     status = None
        
    #     try:
    #         version_float = float(version)
    #     except ValueError:
    #         return Response({'status': 'Invalid version number format = ' + version}, status=400)

    #     # if float(settings.APP_VERSION) > version_float:
    #     #     status = 'Update available'
    #     # else:
    #     #     status = 'No update available'

    #     data = {'status': status}
    #     serializer = UpdateCheckSerializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data)
    
    
class FirmwareViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows firmware to be viewed or edited.
    """
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Get the firmware data from validated_data
        firmware_file = serializer.validated_data.get('firmware_file')

        # Create the Firmware instance first without the actual content file
        filename = serializer.validated_data['filename']
        chunk_size = serializer.validated_data['chunk_size']
        checked_date = timezone.now()
        firmware_instance = Firmware(firmware_file=filename, chunk_size=chunk_size, checked_date=checked_date)

        # Then save the file using the new Firmware instance as filename
        with open(filename, 'wb') as f:
            f.write(firmware_file.read())
        firmware_instance.save()

