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
        # ✅ Always set total_amount from room price
        if self.room and self.room.price:
            self.total_amount = Decimal(self.room.price)

        # ✅ If no advance given, set default (30% of total_amount)
        if not self.advance_amount or self.advance_amount == 0:
            self.advance_amount = self.total_amount * Decimal("0.3")

        # ✅ Prevent advance > total
        if self.advance_amount > self.total_amount:
            self.advance_amount = self.total_amount

        # ✅ Balance = total - advance
        self.balance_amount = self.total_amount - self.advance_amount

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.id} - {self.hotel.hotal_name} - {self.room.room_type}"
