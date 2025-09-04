import os
import requests
from ..models import Location, Weather, CurrentWeather

from api.config.endpoints import ENDPOINTS

def fetch_weather_from_api(lat, lon, units="metric"):
    api_key = os.getenv("WEATHERMAP_API_KEY")
    url = (
        f"{ENDPOINTS['current_weather']}?"
        f"lat={lat}&lon={lon}&units={units}&appid={api_key}"
    )
    return requests.get(url)


def save_weather_data(response_json, precise_name=None, state=None):
    location_data = {
        "id": response_json.get("id"),
        "name": response_json.get("name"),
        "precise_name": precise_name.strip() if precise_name else "Not defined",
        "state": state.strip() if state else "Not defined",
        "lat": response_json.get("coord", {}).get("lat"),
        "lon": response_json.get("coord", {}).get("lon"),
        "country": response_json.get("sys", {}).get("country"),
        "population": 0,
        "timezone": response_json.get("timezone"),
        "sunrise": response_json.get("sys", {}).get("sunrise"),
        "sunset": response_json.get("sys", {}).get("sunset"),
    }

    location, _ = Location.objects.update_or_create(
        id=location_data["id"], defaults=location_data
    )

    weather_data = {
        "weather_main": response_json.get("weather", [{}])[0].get("main"),
        "weather_description": response_json.get("weather", [{}])[0].get("description"),
        "weather_icon": response_json.get("weather", [{}])[0].get("icon"),
        "base": response_json.get("base"),
        "temp": response_json.get("main", {}).get("temp"),
        "feels_like": response_json.get("main", {}).get("feels_like"),
        "temp_min": response_json.get("main", {}).get("temp_min"),
        "temp_max": response_json.get("main", {}).get("temp_max"),
        "pressure": response_json.get("main", {}).get("pressure"),
        "humidity": response_json.get("main", {}).get("humidity"),
        "sea_level": response_json.get("main", {}).get("sea_level", 0),
        "grnd_level": response_json.get("main", {}).get("grnd_level", 0),
        "visibility": response_json.get("visibility", 0),
        "wind_speed": response_json.get("wind", {}).get("speed", 0.0),
        "wind_deg": response_json.get("wind", {}).get("deg", 0),
        "wind_gust": response_json.get("wind", {}).get("gust", 0.0),
        "rain_1h": response_json.get("rain", {}).get("1h", 0.0),
        "snow_1h": response_json.get("snow", {}).get("1h", 0.0),
        "clouds_all": response_json.get("clouds", {}).get("all", 0),
        "dt": response_json.get("dt"),
    }

    weather, _ = Weather.objects.update_or_create(
        id=location_data["id"], defaults=weather_data
    )

    current_weather, _ = CurrentWeather.objects.update_or_create(
        location=location, defaults={"weather": weather}
    )

    return current_weather
