
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate


from api.v1.hotel.serializers import *
from api.v1.customer.serializers import *
from Hotel.models import *




@api_view(['GET'])
@permission_classes([AllowAny])
def hotel(request):
    instance = Hotal.objects.all()
    context = {
        'request':request
    }
    serializers = HotelSerializer(instance, many=True, context=context)

    response_data = {
       'status_code' : 6000,
       'data' : serializers.data,
       'message' : 'Hotel list retrieved successfully'
    }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def hotel_search(request):
    instance = Hotal.objects.all()
    location = request.GET.get('location')

    if location:
        instance = Hotal.objects.filter(
            location__icontains=location,

    )
    elif location:
        instance = Hotal.objects.filter(location__icontains=location)

    else:
        instance = Hotal.objects.all()
    context = {
        'request':request
    }
    serializers = HotelSerializer(instance, many=True, context=context)

    response_data = {
       'status_code' : 6000,
       'data' : serializers.data,
       'message' : 'Hotel search  successfully'
    }
    return Response(response_data)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_hotel(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    instance = Hotal.objects.get(id=id)
    

    room = Room.objects.filter(hotel_id=instance)
    
    context = {
        'request': request
    }
    serializers = HotelSerializer(instance, context=context)
    response_data = {
        'status_code': 6000,
        'data': {
            'hotel': serializers.data,
            # 'rooms': RoomSerializer(room, many=True, context=context).data
        },
        'message': 'Hotel details retrieved successfully'
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hotel_manager(request):
    user = request.user
    hotel_manager = Hotal.objects.get(manager = user)
    
        # Get the hotel assigned to the logged-in manager
    room = Room.objects.filter(hotel_id = hotel_manager)
    context = {
        'request': request
    }
    serializers = HotelSerializer(hotel_manager, context=context)
    response_data = {
        'status_code': 6000,
        'data': {
            'hotel': serializers.data,
            # 'rooms': RoomSerializer(room, many=True, context=context).data
            
        },
        'message': 'Hotel details retrieved successfully'
    }
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def hotel_create(request):
    context = {
        'request':request
    }
    serializer = HotelSerializer(data = request.data,context=context)
    if serializer.is_valid():
        serializer.save()
        
        response_data = {
            'status_code': 6000,
            'data': serializer.data,
            'message': 'Hotal created successfully'
        }
        return Response(response_data)
    else:
        response_data = {
            'status_code':6001,
            'error':serializer.errors,
            'message':'Hotal creation failed'
        }
        return Response(response_data)
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def hotel_edit(request,id):
    user = request.user
    instance = Hotal.objects.get(id=id, manager=user)
   
    hotal_name = request.data.get('hotal_name')
    image = request.data.get('image')
    description = request.data.get('description')
    phone = request.data.get('phone')
    rating = request.data.get('rating')
    location = request.data.get('location')
    email = request.data.get('email')
    amentities = request.data.get('amentities')
    # is_active = request.data.get('is_active')


    instance.hotal_name = hotal_name
    instance.image = image
    instance.description = description
    instance.phone = phone
    instance.rating = rating
    instance.location = location
    instance.email = email
    instance.amentities = amentities
    # instance.is_active = is_active
    instance.save()

    response_data = {
        'status_code':6001,
        'message':'Hotal updated successfully'
    }
    return Response(response_data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def hotel_deleted(request, id):
   instance = Hotal.objects.get(id=id)
   instance.delete()

   response_data = {
       "status_code": 6000,
       "data": {},
       "message": "Address deleted successfully"
   }
   return Response(response_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def top_rated_hotels(request):
    # Get top 5 hotels by rating
    hotels = Hotal.objects.order_by('-rating')[:5]
    serializer = HotelSerializer(hotels, many=True)
    return Response(serializer.data)