# import os
# from django.shortcuts import render
# from rest_framework.decorators import api_view
from .serializers import ErrorLogSerializer, UpdateCheckSerializer, FirmwareSerializer, UserSerializer, GroupSerializer
from django.contrib.auth.models import User, Group
from .models import ErrorLog, UpdateCheck, Firmware
from rest_framework import viewsets
from rest_framework import permissions
from django.utils import timezone
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

