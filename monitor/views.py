from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Service, Monitor_Log
from .serializer import ServiceSerializer, MonitorLogSerializer

# Create your views here.
@api_view(['GET'])
def get_services(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_service(request):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def get_service(request, id):
#     service = Service.objects.get(id = id)
#     serializer = ServiceSerializer(service)
#     return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def get_service(request, id):
    """
    Retrieve, update or delete a service.
    """
    try:
        service = Service.objects.get(id = id)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def get_recommendation(request, service_id):
    from openai import OpenAI
    client = OpenAI()

    service = Service.objects.get(id = service_id)

    latest_monitor_log = Monitor_Log.objects.filter(service = service).order_by('-id')[:1].first()

    print(service.architecture)
    print(latest_monitor_log.status_code)

    if latest_monitor_log.status_code != 200:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to help system technicians in fixing the server issues."},
                {"role": "system", "content": "{}".format(service.architecture)},
                {"role": "user", "content": "I checked the system, but the HTTP status is {}. Can you tell the possible solution?".format(latest_monitor_log.status_code)}
            ]
        )
        print(completion.choices[0].message.content)
        return Response({'recommendation' : completion.choices[0].message.content})
    else:
        return Response({'recommendation' : 'The service is up and running fine! :)'})