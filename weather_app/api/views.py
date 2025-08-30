import os

import requests
from django.http import JsonResponse
from dotenv import load_dotenv
from rest_framework.views import APIView

from api.models import *

load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))


class LocationView(APIView):
    def get(self, request):
        q = request.GET.get('q')
        if not q:
            return JsonResponse(
                {'error': 'Missing query parameter'}, 
                status=400
            )

        try:
            parts = [p.strip() for p in q.split(',')]

            city_name = ""
            state_code = ""
            country_code = ""

            if len(parts) == 1:
                city_name = parts[0]
            elif len(parts) == 2:
                city_name = parts[0]
                country_code = parts[1]
            elif len(parts) == 3:
                city_name = parts[0]
                state_code = parts[1]
                country_code = parts[2]
            else:
                return JsonResponse(
                    {'error': 'Invalid query format'}, 
                    status=400
                )

        except Exception as exc:
            return JsonResponse({'error': str(exc)}, status=400)

        api_key = os.getenv("WEATHERMAP_API_KEY")
        url = (
            f"http://api.openweathermap.org/geo/1.0/direct?"
            f"q={city_name},{state_code},{country_code}&limit=5&appid={api_key}"
        )

        response = requests.get(url)
        if response.status_code == 200:
            if response.json() == []:
                return JsonResponse(
                    {'error': 'No locations found'},
                    status=404
                )
            response_data = response.json()
            for location in response_data:
                location.pop('local_names', None)
            return JsonResponse(response_data, safe=False)
        return JsonResponse(
            {'error': 'Failed to fetch location data'}, 
            status=response.status_code
        )


class CurrentWeatherView(APIView):
    def get(self, request):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        units = request.GET.get('units', 'metric')

        if not lat or not lon:
            return JsonResponse(
                {'error': 'Missing latitude or longitude parameter'}, 
                status=400
            )

        if units and units not in ['standard', 'metric', 'imperial']:
            units = 'metric'

        api_key = os.getenv("WEATHERMAP_API_KEY")
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&units={units}&appid={api_key}"
        )

        response = requests.get(url)
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        return JsonResponse(
            {'error': 'Failed to fetch weather data'}, 
            status=response.status_code
        )
