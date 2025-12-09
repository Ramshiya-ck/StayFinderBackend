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
    customer_email = serializers.EmailField(source='customer.user.email', read_only=True)
    customer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['id', 'customer', 'customer_email', 'customer_name', 'phone', 'address', 'city', 'country', 'profile_image', 'is_default']
        read_only_fields = ['customer', 'customer_email', 'customer_name']
    
    def get_customer_name(self, obj):
        return f"{obj.customer.user.first_name} {obj.customer.user.last_name}"


