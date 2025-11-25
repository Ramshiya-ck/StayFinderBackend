from django.urls import path
from . import views

urlpatterns = [
    path('request/create/',views.request_create,name='request_create'),
]