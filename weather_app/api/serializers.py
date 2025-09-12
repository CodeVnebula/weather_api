from rest_framework import serializers
from .models import Location, CurrentWeather


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CurrentWeatherSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    weather = serializers.JSONField(source='current_weather_data')
    last_updated = serializers.DateTimeField()
    
    class Meta:
        model = CurrentWeather
        fields = ['location', 'weather', 'last_updated']


class LocationSearchSerializer(serializers.Serializer):
    name = serializers.CharField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    country = serializers.CharField()
    state = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    
    
class ForecastSerializer(serializers.Serializer):
    location = LocationSerializer()
    forecast_data = serializers.JSONField()
    last_updated = serializers.DateTimeField()
    cnt = serializers.IntegerField()
    
    class Meta:
        fields = ['location', 'forecast', 'last_updated', 'cnt']