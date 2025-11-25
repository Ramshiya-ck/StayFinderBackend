from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from Hotel.models import *


class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotal
        fields = ['id','hotal_name','image','description','phone','rating','location','email','amenities','manager']

class HotelManagerSerializer(ModelSerializer):
    class Meta:
        model = Hotal
        fields = ['id','hotal_name','image','description','phone','rating','location','email','amenities','manager']