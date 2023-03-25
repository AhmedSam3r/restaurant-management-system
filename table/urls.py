from django.urls import path
from . import views
from .views import TableAPIView



urlpatterns = [
    path('', TableAPIView.as_view(), name='table_related_apis'),
]

