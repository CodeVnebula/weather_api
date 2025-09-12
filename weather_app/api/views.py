from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Location, CurrentWeather, Forecast

from .serializers import (
    CurrentWeatherSerializer, 
    ForecastSerializer, 
    LocationSearchSerializer,
)
from api.services.location_service import (
    fetch_locations_from_api,
    clean_location_results,
    extract_location_data,
)
from api.services.weather_service import (
    extract_forecast_data,
    fetch_weather_from_api,
    extract_weather_data,
)

from .config.settings import LOCATION_TOLERANCE, CACHE_EXPIRY

class LocationView(APIView):
    def get(self, request):
        q = request.GET.get("q")
        if not q:
            return Response(
                {"error": "Missing query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        parts = [p.strip() for p in q.split(",")]
        city_name, state_code, country_code = "", "", ""

        if len(parts) == 1:
            city_name = parts[0]
        elif len(parts) == 2:
            city_name, country_code = parts
        elif len(parts) == 3:
            city_name, state_code, country_code = parts
        else:
            return Response(
                {"error": "Invalid query format"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        api_response = fetch_locations_from_api(
            city_name, state_code, country_code
        )

        if api_response.status_code != 200:
            return Response(
                {"error": "Failed to fetch location data"},
                status=api_response.status_code,
            )

        response_json = api_response.json()
        if not response_json:
            return Response(
                {"error": "No locations found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        unique_locations = clean_location_results(response_json)

        serializer = LocationSearchSerializer(unique_locations, many=True)
        return Response(serializer.data)


class CurrentWeatherView(APIView):
    def get(self, request):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        units = request.GET.get('units', 'metric')
        precise_name = request.GET.get('precise_name')
        state = request.GET.get('state')

        if not lat or not lon:
            return Response(
                {"error": "Missing latitude or longitude parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if units not in ['standard', 'metric', 'imperial']:
            units = 'metric'
            
        try:
            lat_rounded = round(float(lat), 4)
            lon_rounded = round(float(lon), 4)
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid latitude or longitude value"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        location = Location.objects.filter(
            lat__gte=lat_rounded - LOCATION_TOLERANCE, 
            lat__lte=lat_rounded + LOCATION_TOLERANCE,
            lon__gte=lon_rounded - LOCATION_TOLERANCE, 
            lon__lte=lon_rounded + LOCATION_TOLERANCE
        ).first()
        
        if location:
            current_weather = CurrentWeather.objects.filter(
                location=location).first()
            if current_weather and current_weather.last_updated:
                if (
                    datetime.now(timezone.utc) - current_weather.last_updated
                ).total_seconds() < CACHE_EXPIRY:
                    return Response({
                        "data": CurrentWeatherSerializer(current_weather).data,
                        "source": "database",
                        "location": {"lat": location.lat, "lon": location.lon},
                        "rounded": {"lat": lat_rounded, "lon": lon_rounded}
                    })

        api_response = fetch_weather_from_api(lat, lon, units)

        if api_response.status_code != 200:
            return Response(
                {"error": "Failed to fetch weather data"},
                status=api_response.status_code,
            )

        current_weather_data = extract_weather_data(api_response.json())
        population = 0
        if location:
            population = location.population
            
        location_data = extract_location_data(response_json=api_response.json(),
                                              state=state,
                                              precise_name=precise_name,
                                              population=population)

        # Remove 'id' if present and ensure all required fields are included
        location_data.pop('id', None)
        lookup_fields = {
            'lat': location_data.get('lat'),
            'lon': location_data.get('lon'),
        }
        update_fields = {
            k: v for k, v in location_data.items() if k not in lookup_fields
        }
        location, _ = Location.objects.update_or_create(
            defaults=update_fields, **lookup_fields
        )
        current_weather, _ = CurrentWeather.objects.update_or_create(
            location=location,
            defaults={'current_weather_data': current_weather_data}
        )
            
        serializer = CurrentWeatherSerializer(current_weather)
        return Response(
            {
                "data": serializer.data,
                "source": "api"
            }
        )
        

class ForecastView(APIView):
    def get(self, request):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        units = request.GET.get('units', 'metric')
        precise_name = request.GET.get('precise_name')
        state = request.GET.get('state')
        
        if not lat or not lon:
            return Response(
                {"error": "Missing latitude or longitude parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if units not in ['standard', 'metric', 'imperial']:
            units = 'metric'
            
        try:
            lat_rounded = round(float(lat), 4)
            lon_rounded = round(float(lon), 4)
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid latitude or longitude value"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        location = Location.objects.filter(
            lat__gte=lat_rounded - LOCATION_TOLERANCE, 
            lat__lte=lat_rounded + LOCATION_TOLERANCE,
            lon__gte=lon_rounded - LOCATION_TOLERANCE, 
            lon__lte=lon_rounded + LOCATION_TOLERANCE
        ).first()
        
        if location:
            forecast = Forecast.objects.filter(location=location).first()
            if forecast and forecast.last_updated:
                if (
                    datetime.now(timezone.utc) - forecast.last_updated
                ).total_seconds() < CACHE_EXPIRY:
                    return Response({
                        "data": ForecastSerializer(forecast).data,
                        "source": "database",
                        "location": {"lat": location.lat, "lon": location.lon},
                        "rounded": {"lat": lat_rounded, "lon": lon_rounded}
                    })
        
        api_response = fetch_weather_from_api(lat, lon, units, mode="forecast")
        
        if api_response.status_code != 200:
            return Response(
                {"error": "Failed to fetch forecast data"},
                status=api_response.status_code,
            )

        forecast_data = extract_forecast_data(api_response.json())
        location_data = extract_location_data(response_json=api_response.json(),
                                              state=state,
                                              precise_name=precise_name)

        # Remove 'id' if present and ensure all required fields are included
        location_data.pop('id', None)
        lookup_fields = {
            'lat': location_data.get('lat'),
            'lon': location_data.get('lon'),
        }
        update_fields = {
            k: v for k, v in location_data.items() if k not in lookup_fields
        }
        location, _ = Location.objects.update_or_create(
            defaults=update_fields, **lookup_fields
        )
        forecast, _ = Forecast.objects.update_or_create(
            location=location,
            defaults={
                'forecast_data': forecast_data,
                'cnt': api_response.json().get('cnt', len(forecast_data))
            }
        )

        serializer = ForecastSerializer(forecast)
        return Response(
            {
                "data": serializer.data,
                "source": "api"
            }
        )
