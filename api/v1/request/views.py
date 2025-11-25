from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from api.v1.request.serializers import *
from Request.models import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_create(request):
    user = request.user
    context = {
        'request': request
    }
    serializers = RequestSerializer(data = request.data, context=context)
    if serializers.is_valid():
        serializers.save(user=user)
        response_data = {
            "status_code": 6000,
            "data": serializers.data,
            "message": "Request created successfully"
        }
        return Response(response_data)
    else:
        response_data = {
            "status_code": 6001,
            "errors" : serializers.errors,
            "message": "Something went wrong"
        }
        return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def request_form(request):
    user = request.user
    instance = Request.objects.all()
    context = {
        'request' : request
    }  
    serializers = RequestSerializer(instance, many=True, context=context)
    response_data = {
        "status_code": 6000,
        "data" : serializers.data,
        "message": "Request list retrieved successfully"
    }
    return Response(response_data)


@api_view(['DELETE'])
@permission_classes(IsAuthenticated)
def request_delete(request,id):
    user = request.user
    instance = Request.objects.get(id=id)
    instance.delete()
    response_data = {
        "status":6000,
        "data":{},
        "message": "request deleted sucessfully"
    }
    Response(response_data)
    


    


