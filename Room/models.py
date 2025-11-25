from django.db import models
from Hotel.models import *
from user.models import *

class Room(models.Model):
    ROOM_TYPES = [
        ('single','Single'),
        ('double','Double'),
        ('suit','Suit')
    ]
    image = models.FileField(upload_to='roomimages',blank=True,null=True)
    hotel_id = models.ForeignKey(Hotal,on_delete=models.CASCADE,related_name='rooms')
    room_type = models.CharField(max_length=255,choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    availability = models.BooleanField(default=True)

    class Meta:
        db_table = 'hotel_rooms'
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ['-id']

    def __str__(self):
        return self.room_type

    




