from django.urls import path

from . import views


app_name = "health"
urlpatterns = [
    path("results.html", views.results, name="results"),
    path("", views.index, name="index"),
]