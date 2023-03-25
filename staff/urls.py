from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', views.login, name='login_user'),
    path('create/', views.create_user, name='create_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),          
]

