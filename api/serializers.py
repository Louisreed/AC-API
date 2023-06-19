from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import ErrorLog, UpdateCheck, Firmware
    
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        
        
class ErrorLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ErrorLog
        fields = '__all__'
        
        
class UpdateCheckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UpdateCheck
        fields = ['version', 'checked_date']


class FirmwareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Firmware
        fields = ['checked_date', 'firmware_file']