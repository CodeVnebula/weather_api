from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Location, CurrentWeather

from .serializers import CurrentWeatherSerializer, LocationSearchSerializer
from api.services.location_service import (
    fetch_locations_from_api,
    clean_location_results,
)
from api.services.weather_service import (
    fetch_weather_from_api,
    save_weather_data,
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

        current_weather = save_weather_data(
            api_response.json(), precise_name, state
        )

        serializer = CurrentWeatherSerializer(current_weather)
        return Response(
            {
                "data": serializer.data,
                "source": "api"
            }
        )