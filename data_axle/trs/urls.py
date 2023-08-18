from django.urls import path,include
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('check_availability/',check_availability, name='check_availability'),
    path('reserve_seats/',reserve_seats, name = 'reserve_seats'),
    
]