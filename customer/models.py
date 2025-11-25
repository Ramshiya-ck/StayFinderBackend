from django.db import models
from user.models import User
import random


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email

class Profile(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='profiles'
    )
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    profile_image = models.FileField(upload_to='profile_images', blank=True, null=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'customer_profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if self.is_default:
            Profile.objects.filter(customer=self.customer, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.user.email}-Profile"


        


    




