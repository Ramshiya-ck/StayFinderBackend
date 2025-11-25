from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from Request.models import Request
from Hotel.models import Hotal

class RequestSerializer(ModelSerializer):
    class Meta:
        model = Request
        fields = ["id", 'user', 'hotel_name', 'address', 'description', 'email','phone','location', 'created_at', 'updated_at']
        hotel_name = serializers.SlugRelatedField(
        queryset=Hotal.objects.all(),
        slug_field='name'   # this will allow passing hotel name
    )