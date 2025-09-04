from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CurrentWeatherSerializer, LocationSearchSerializer
from api.services.location_service import (
    fetch_locations_from_api,
    clean_location_results,
)
from api.services.weather_service import (
    fetch_weather_from_api,
    save_weather_data,
)

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
        return Response(serializer.data)