from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from api.v1.room.serializers import *
from Room.models import *
from Hotel.models import Hotal



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rooms(request,hotel_id):  
    rooms = Room.objects.filter(hotel_id=hotel_id)


    context = {
        'request': request}
    if not rooms.exists():
        return Response({
            'status_code': 404,
            'data': [],
            'message': 'No rooms found for this hotel'
        })

    serializer = RoomSerializer(rooms, many=True, context=context)
    return Response({
        'status_code': 200,
        'data': serializer.data,
        'message': 'Rooms retrieved successfully'
    })
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_single_detail(request, room_id):
    manager = request.user
    hotel = Hotal.objects.get(manager=manager)   # logged-in manager’s hotel

    # safer query
    room = Room.objects.filter(id=room_id, hotel_id=hotel.id).first()

    if not room:
        return Response(
            {"status_code": 4004, "message": "Room not found for this manager"},
            status=404,
        )

    serializer = RoomSerializer(room, context={'request': request})
    return Response(
        {"status_code": 6000, "data": serializer.data, "message": "Room details retrieved successfully"}
    )



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def room_create(request, hotel_id):
    hotel = Hotal.objects.get(id=hotel_id)  # use id here
    context = {
        'request': request,
        'hotel': hotel   # pass hotel to serializer context
    }
    serializer = RoomSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()  # hotel is attached in serializer
        return Response({
            'status_code': 6000,
            'data': serializer.data,
            'message': 'Room created successfully'
        })
    return Response({
        'status_code': 6001,
        'error': serializer.errors,
        'message': 'Room creation failed'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_search(request, id):
    instance = Room.objects.filter(id=id)

    price = request.GET.get('price')
    room_type = request.GET.get('room_type')

    if price:
        instance = Room.objects.filter(
            price__lte=price
        )
    elif room_type:
        instance = Room.objects.filter(
            room_type__icontains=room_type
        )

    else:
        instance = Room.objects.all()

    context = {
        'request': request
    }    
    serializers = RoomSerializer(instance,many=True, context=context)
    response_data = {
        'status_code': 6000,
        'data': serializers.data,
        'message': 'Room search successfully'
    }
    return Response(response_data)


    
@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def room_edit(request, id):
    instance = Room.objects.get(id=id)
    hotel_id = request.data.get('hotel')
    if hotel_id:
        
            hotel_instance = Hotal.objects.get(id=int(hotel_id))
            instance.hotel = hotel_instance

            return Response({
                'status_code': 6001,
                'message': 'Invalid hotel id'
            }, status=400)

    if 'image' in request.data:
        instance.image = request.data['image']
    if 'room_type' in request.data:
        instance.room_type = request.data['room_type']
    if 'price' in request.data:
        instance.price = request.data['price']
    if 'availability' in request.data:
        availability = request.data['availability']
    if isinstance(availability, str):  # convert string → boolean
        availability = availability.lower() in ['true', '1', 'yes']
    instance.availability = availability


    instance.save()

    return Response({
        'status_code': 6000,
        'message': 'Room updated successfully'
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def room_deleted(request, id):
   instance = Room.objects.get(id=id)
   instance.delete()

   response_data = {
       "status_code": 6000,
       "data": {},
       "message": "Room deleted successfully"
   }
   return Response(response_data)