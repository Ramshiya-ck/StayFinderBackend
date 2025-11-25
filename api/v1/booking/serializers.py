from rest_framework import serializers
from  booking.models import Booking
from Room.models import Room

class BookingSerializer(serializers.ModelSerializer):
   class Meta:
        model = Booking
        fields = ['id', 'customer', 'hotel', 'room', 'address', 'phone', 'payment_status','guests', 'check_in', 'check_out', 'total_amount', 'advance_amount', 'balance_amount', 'booking_status', 'created_at', 'updated_at']
        read_only_fields = ['balance_amount', 'created_at', 'updated_at']

