from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from Hotel.models import *
from Room.models import *
from booking.models import *
from user.models import *
from customer.models import *



class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','user']




class SliderSerializer(ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id','name','image','description']       


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','phone','address','city','country','profile_image','is_default']


