# some_app/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import CurrentWeather, Forecast

@shared_task
def cleanup_old_weather_data():
    """
    Task to clean up weather data older than 1 day.
    """
    threshold_date = timezone.now() - timezone.timedelta(days=1)
    CurrentWeather.objects.filter(last_updated__lt=threshold_date).delete()
    Forecast.objects.filter(last_updated__lt=threshold_date).delete()
