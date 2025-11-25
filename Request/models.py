from django.db import models


from django.db import models
from Hotel.models import Hotal
from user.models import User

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_name = models.ForeignKey(Hotal, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    class Meta:
        db_table = 'hotel_requests'
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'
        ordering = ['-id']
    def __str__(self):
        return f"Request #(self.id)-(self.hotel_name)-(self.status)"
    