from django.urls import path, include
from . import views

urlpatterns = [
    path('events', views.events),
    path('', views.home),
]