from django.urls import path
from tracking import views


urlpatterns = [
    path('', views.list_sightings),
    path('add', views.add_sighting),
    path('stats', views.stats),
    path('<str:pk>', views.update_or_delete)
]
