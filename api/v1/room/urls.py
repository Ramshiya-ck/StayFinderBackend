from django.urls import path
from api.v1.room import views

urlpatterns=[
    path('rooms/<int:hotel_id>/',views.rooms,name='rooms'),
    path('room/single/detail/<int:room_id>/',views.room_single_detail,name='rooms'),
    path('room/create/<int:hotel_id>/',views.room_create,name='room_create'),
    path('room/edit/<int:id>/',views.room_edit,name='room_edit'),
    path('room/delete/<int:id>/',views.room_deleted,name='room_deleted'),
    path('room/search/<int:id>/',views.room_search,name='room_search'),
]