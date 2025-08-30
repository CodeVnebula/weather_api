from django.urls import path
from api import views

urlpatterns = [
    path('search-locations/', views.LocationView.as_view(), name='location'),
    path('current-weather/', views.CurrentWeatherView.as_view(), name='current_weather'),
]
