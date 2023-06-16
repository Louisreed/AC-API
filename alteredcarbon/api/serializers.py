from django.contrib.auth.models import User, Group
from .models import ErrorLog, UpdateCheck, Firmware
from rest_framework import serializers
    
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        
        
class ErrorLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ErrorLog
        fields = ['message', 'stack_trace', 'created']
        
class UpdateCheckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UpdateCheck
        fields = ['version', 'checked_date']
        
class FirmwareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Firmware
        fields = ['filename', 'chunk_size', 'checked_date']
        
        
# class ErrorLogSerializer(serializers.Serializer):
#     element = serializers.CharField()
#     value = serializers.CharField()


# class UpdateCheckSerializer(serializers.Serializer):
#     ver = serializers.CharField()


# class FirmwareDownloadSerializer(serializers.Serializer):
#     gsf = serializers.IntegerField()
#     gdf = serializers.IntegerField()
#     chunk = serializers.IntegerField()
