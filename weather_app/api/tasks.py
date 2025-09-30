from celery import shared_task
from django.utils import timezone
from .models import CurrentWeather, Forecast

@shared_task
def cleanup_old_weather_data():
    threshold_date = timezone.now() - timezone.timedelta(days=2)
    batch_size = 1000
    qs = CurrentWeather.objects.filter(last_updated__lt=threshold_date)
    while qs.exists():
        qs[:batch_size].delete()
    qs = Forecast.objects.filter(last_updated__lt=threshold_date)
    while qs.exists():
        qs[:batch_size].delete()