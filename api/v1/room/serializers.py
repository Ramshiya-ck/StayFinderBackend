from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from Room.models import *

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','image','hotel_id','room_type','price','availability']