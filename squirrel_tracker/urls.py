from django.contrib import admin
from django.urls import path, include
from tracking.views import map_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sightings/', include('tracking.urls')),
    path('map/', map_view)
]
