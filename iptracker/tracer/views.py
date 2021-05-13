from django.http import response
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    TraceSerializer,
)
from .models import IpRecord
from .services import get_geolocation
from .utils import ip_is_valid


@api_view(['POST'])
def trace_ip(request):
    input_ip = request.data.get('ip')
    if input_ip and ip_is_valid(input_ip):
        try:
            ip_obj = IpRecord.objects.get(ip=input_ip)
            response_serializer = TraceSerializer(ip_obj)
        except IpRecord.DoesNotExist:
            ip_data = get_geolocation(input_ip)
            if ip_data['status'] != 'fail':
                response_serializer = TraceSerializer(data=ip_data)
                if response_serializer.is_valid():
                    response_serializer.save()
                else:
                    return Response(response_serializer.errors)
            else:
                return Response({'error': 'Something went wrong, please try again.'})
        return Response(response_serializer.data)
    return Response(
        {'ip': 'Please enter a valid ip address'},
        status=403
    )


@api_view(['GET'])
def ip_statistics(request):
    furthest_trace = IpRecord.objects.get_longest_distance()
    most_traced = IpRecord.objects.get_most_traced()
    if furthest_trace or most_traced:
        return Response({
            'longest_distance': {**furthest_trace},
            'most_traced': {**most_traced}
        })
    return Response({"ip_statistics"})
