from django.db import models
    

class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    
    lat = models.FloatField()
    lon = models.FloatField()
    
    country = models.CharField(max_length=50)
    population = models.IntegerField()
    
    timezone = models.IntegerField()
    
    sunrise = models.IntegerField()
    sunset = models.IntegerField()


class Weather(models.Model):
    weather_main = models.CharField(max_length=50)
    weather_description = models.CharField(max_length=100)    
    weather_icon = models.CharField(max_length=10)

    base = models.CharField(max_length=50)
    
    temp = models.FloatField()
    feels_like = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    pressure = models.IntegerField()
    humidity = models.IntegerField()
    sea_level = models.IntegerField()
    grnd_level = models.IntegerField()
    
    visibility = models.IntegerField()
    
    wind_speed = models.FloatField()
    wind_deg = models.IntegerField()
    wind_gust = models.FloatField()
    
    rain_1h = models.FloatField()
    
    snow_1h = models.FloatField()
    
    clouds_all = models.IntegerField()
    
    dt = models.IntegerField()


class CurrentWeather(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    weather = models.OneToOneField(Weather, on_delete=models.CASCADE)