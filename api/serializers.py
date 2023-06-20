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
        fields = ['id', 'value', 'created']
        
        
class UpdateCheckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UpdateCheck
        fields = ['id', 'version', 'checked_date']


class FirmwareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Firmware
        fields = ['firmware_file', 'checked_date']