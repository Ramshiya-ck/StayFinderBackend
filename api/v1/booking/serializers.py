from rest_framework import serializers
from  booking.models import Booking
from Room.models import Room

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'customer', 'hotel', 'room', 'address', 'phone', 'payment_status','guests', 'check_in', 'check_out', 'total_amount', 'advance_amount', 'balance_amount', 'booking_status', 'created_at', 'updated_at']
        read_only_fields = ['total_amount', 'balance_amount', 'created_at', 'updated_at']
    
    def update(self, instance, validated_data):
        # Check if dates are being changed
        dates_changed = 'check_in' in validated_data or 'check_out' in validated_data
        
        # If dates changed and advance_amount not explicitly provided, reset it to trigger recalculation
        if dates_changed and 'advance_amount' not in validated_data:
            validated_data['advance_amount'] = 0  # This will trigger 30% recalculation in model.save()
        
        return super().update(instance, validated_data)

