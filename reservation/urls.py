from django.urls import path
from . import views


urlpatterns = [
    path('check/', views.check_available_time_slots, name='check_available_time_slots'),
    path('add/', views.reserve_time_slot, name='reserve_time_slot'),
    path('delete/', views.delete_reservation, name='delete_reservation'),
    path('retrieve/today/', views.get_reservations_today, name='get_reservations_today'),
    path('retrieve/history/', views.get_reservations_history, name='get_reservations_history'),
]

