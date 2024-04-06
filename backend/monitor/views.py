from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Service, Monitor_Log
from .serializer import ServiceSerializer, MonitorLogSerializer

# Create your views here.
@api_view(['GET'])
def get_services(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)