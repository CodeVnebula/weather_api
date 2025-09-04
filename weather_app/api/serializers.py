from rest_framework import serializers
from .models import Location, Weather, CurrentWeather


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'


class CurrentWeatherSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    weather = WeatherSerializer()

    class Meta:
        model = CurrentWeather
        fields = ['location', 'weather']


class LocationSearchSerializer(serializers.Serializer):
    name = serializers.CharField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    country = serializers.CharField()
    state = serializers.CharField(required=False, allow_null=True, allow_blank=True)