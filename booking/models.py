from django.db import models
from user.models import User
from Hotel.models import Hotal
from Room.models import Room
from decimal import Decimal


class Booking(models.Model):

    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotal, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ✅ advance payment
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # auto-calculated

    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'booking_list'
        verbose_name = 'booking'
        verbose_name_plural = 'bookings'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        # ✅ Validate dates
        if self.check_in and self.check_out:
            if self.check_out <= self.check_in:
                from django.core.exceptions import ValidationError
                raise ValidationError("Check-out date must be after check-in date")
        
        # Store old values for logging
        old_total = getattr(self, 'total_amount', 0)
        old_advance = getattr(self, 'advance_amount', 0)
        old_balance = getattr(self, 'balance_amount', 0)
        
        # ✅ Calculate total_amount from room price × number of nights
        if self.room and self.room.price and self.check_in and self.check_out:
            number_of_nights = (self.check_out - self.check_in).days
            if number_of_nights < 1:
                from django.core.exceptions import ValidationError
                raise ValidationError(f"Invalid booking duration: {number_of_nights} nights")
            
            # Calculate new total
            new_total = Decimal(self.room.price) * Decimal(number_of_nights)
            
            # If total amount changed and advance was based on old total, recalculate advance
            if hasattr(self, 'pk') and self.pk:  # Existing booking being updated
                old_booking = Booking.objects.filter(pk=self.pk).first()
                if old_booking and old_booking.total_amount != new_total:
                    # Total changed - check if advance should be recalculated
                    # If advance was exactly 30% of old total, recalculate it
                    if old_booking.advance_amount == old_booking.total_amount * Decimal("0.3"):
                        self.advance_amount = 0  # Reset to trigger recalculation
            
            self.total_amount = new_total

        # ✅ If no advance given, set default (30% of total_amount)
        if not self.advance_amount or self.advance_amount == 0:
            self.advance_amount = self.total_amount * Decimal("0.3")

        # ✅ Prevent advance > total
        if self.advance_amount > self.total_amount:
            self.advance_amount = self.total_amount

        # ✅ Balance = total - advance (ALWAYS recalculate)
        self.balance_amount = self.total_amount - self.advance_amount
        
        # Log changes for debugging
        if old_total != self.total_amount or old_advance != self.advance_amount or old_balance != self.balance_amount:
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Booking {getattr(self, 'pk', 'new')} recalculated - "
                       f"Total: {old_total}→{self.total_amount}, "
                       f"Advance: {old_advance}→{self.advance_amount}, "
                       f"Balance: {old_balance}→{self.balance_amount}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.id} - {self.hotel.hotal_name} - {self.room.room_type}"
