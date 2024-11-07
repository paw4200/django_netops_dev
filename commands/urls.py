from django.urls import path

from . import views


app_name = "commands"
urlpatterns = [
    path("", views.index, name="index"),
    path("results.html", views.results, name="results"),
]