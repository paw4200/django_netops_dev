from django.urls import path

from . import views


app_name = "discover"
urlpatterns = [
    path("", views.index, name="index"),
    path("map.html", views.map, name="map"),
]