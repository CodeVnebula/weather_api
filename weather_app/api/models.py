from django.db import models
    

class Location(models.Model):
    name = models.CharField(max_length=100)
    precise_name = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    
    lat = models.FloatField()
    lon = models.FloatField()
    
    country = models.CharField(max_length=10)
    population = models.IntegerField()
    timezone = models.IntegerField()
    
    sunrise = models.IntegerField()
    sunset = models.IntegerField()


class CurrentWeather(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    current_weather_data = models.JSONField(null=True, blank=True, default=dict)
    last_updated = models.DateTimeField(auto_now=True)
    
class Forecast(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    forecast_data = models.JSONField(null=True, blank=True, default=dict)
    last_updated = models.DateTimeField(auto_now=True)
    cnt = models.IntegerField(null=True, blank=True)
    