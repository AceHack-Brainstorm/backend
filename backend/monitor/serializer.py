from rest_framework import serializers
from .models import Service, Monitor_Log

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields=('name','url', 'architecture', 'recommendation')

class MonitorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor_Log
        fields=('datetime','status', 'ping', 'service')