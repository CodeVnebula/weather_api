from django.urls import path
from api import views

urlpatterns = [
    path('locations/', views.LocationView.as_view(), name='location'),
    path('current/', views.CurrentWeatherView.as_view(), name='current_weather'),
    path('forecast/', views.ForecastView.as_view(), name='weather_forecast'),
    path('health/', views.HealthCheckView.as_view(), name='health_check'),
]
