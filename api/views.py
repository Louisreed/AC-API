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
import re, os
from .serializers import UserSerializer, GroupSerializer, ErrorLogSerializer, UpdateCheckSerializer, FirmwareSerializer

"""
Variables
"""

chunk_size = int(settings.CHUNK_SIZE)

"""
Helpers
"""

def get_file_size(size_bytes):
    """
    Convert the given number of bytes to a human-readable format (e.g., KB, MB, GB).
    """
    if size_bytes == 0:
        return "0B"  # Special case

    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return "{:.2f} {}".format(size_bytes, size_names[i])


def get_number_of_chunks(firmware_file, chunk_size):
    num_chunks = firmware_file / chunk_size
    return num_chunks


"""
API Endpoint Views
"""

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
    
    def retrieve(self, request, pk=None):
        
        update_check = self.get_object()
        version = update_check.version
        checked_date = update_check.checked_date
        
        # print("updated")
        
        if float(settings.APP_VERSION) > float(version):
            data = {
                'version': version, 
                'checked_date': checked_date, 
                'status': 'update_available'
                }
        else:    
            data = {
                'version': version, 
                'checked_date': checked_date, 
                'status': 'system_upto_date'
                }
        
        return Response(data)
    
    
class FirmwareViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows firmware to be viewed or edited.
    """
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer
    permission_classes = [permissions.IsAuthenticated]
            
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        checked_date = str(instance.checked_date)
        filename = str(instance.filename)
        firmware_id = instance.id
        firmware_file = str(instance.firmware_file)
        num_chunks = get_number_of_chunks(instance.firmware_file.size, chunk_size)

        # print('firmware name: ' + filename)
        # print('firmware file: ' + firmware_file)
        # print('firmware file size:', get_file_size(instance.firmware_file.size))
        # print('chunks: ' + str(num_chunks))

        data = {
            'id: ' + str(firmware_id),
            'filename: ' + filename,
            'checked_date: ' + checked_date,
            'firmware_file: ' + firmware_file,
            'file_size: ' + get_file_size(instance.firmware_file.size),
            'chunks: ' + str(num_chunks)
            }
        
        return Response(data)
    

