
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),


    path('api/v1/customer/', include("api.v1.customer.urls")),
    path('api/v1/hotel/', include("api.v1.hotel.urls")),
    path('api/v1/room/', include("api.v1.room.urls")),
    path('api/v1/booking/', include("api.v1.booking.urls")),


]

if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

    )
