from django.db import models
from django.db import models
from user.models import User
from Hotel.models import Hotal
from Room.models import Room 
from booking.models import Booking




class Payment(models.Model):
        
    PAYMENT_STATUS_CHOICES = [
        ('pending','Pending'),
        ('paid','Paid'),
        ('failed','Failed')
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments',default='0')
    amount = models.DecimalField(max_digits=10, decimal_places=2,default='0')
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    stripe_checkout_session_id = models.CharField(max_length=255, blank=True, null=True)
    

    def __str__(self):
        return f"Payment #{self.id} - {self.booking.id} - {self.status}"


    class Meta:

        db_table = 'payment_list'
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
        ordering = ['-id']