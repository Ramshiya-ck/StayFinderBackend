from django.db import models
from user.models import User
from django.utils import timezone
from django.conf import settings



class Hotal(models.Model):

    hotal_name = models.CharField(max_length=25, unique=True)
    image = models.FileField(upload_to='hotel_images', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    rating = models.FloatField(default=3)
    location = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    amenities = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    manager = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="hotel")
    

    class Meta:
        db_table = 'Hotel'
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'
        ordering = ['-id']


    def __str__(self):
        return str(self.hotal_name)
    
# class HotelManager(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     hotel = models.ForeignKey(Hotal,on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'Hotel_manager'
#         verbose_name =  'Hotel_Manager'
#         verbose_name_plural = 'Hotel_managers'
#         ordering = ['-id']

#         def __str__(self):
#             return self.user.email

class Slider(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='slider_images',blank=True,null=True)
    description = models.TextField(blank=True,null=True)

    class Meta:
        db_table = 'Hotel_slider'
        verbose_name = 'Slider'
        verbose_name_plural = 'Sliders'
        ordering = ['-id']

        def __str__(self):
            return self.name



