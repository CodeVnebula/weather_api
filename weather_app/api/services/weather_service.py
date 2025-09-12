import os
import requests

from api.config.endpoints import ENDPOINTS

def fetch_weather_from_api(lat, lon, units="metric", mode="current"):
    api_key = os.getenv("WEATHERMAP_API_KEY")
    url_current = (
        f"{ENDPOINTS['current_weather']}?"
        f"lat={lat}&lon={lon}&units={units}&appid={api_key}"
    )
    url_forecast = (
        f"{ENDPOINTS['weather_forecast']}?"
        f"lat={lat}&lon={lon}&units={units}&appid={api_key}"
    )
    
    if mode == "forecast":
        return requests.get(url_forecast)
    elif mode == "current":
        return requests.get(url_current)
    else:
        # This should never happen if the function is used correctly,
        # but just in case
        raise ValueError(
            "Invalid mode in function fetch_weather_from_api"
            "(api/services/weather_service.py)"
        )


def extract_weather_data(response_json):
    weather_data = {
        "weather_main": response_json.get("weather", [{}])[0].get("main"),
        "weather_description": response_json.get(
            "weather", [{}])[0].get("description"),
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
        
        "pod": response_json.get("sys", {}).get("pod", None),
        "pop": response_json.get("pop", None),
        
        "wind_speed": response_json.get("wind", {}).get("speed", 0.0),
        "wind_deg": response_json.get("wind", {}).get("deg", 0),
        "wind_gust": response_json.get("wind", {}).get("gust", 0.0),
        
        "rain": response_json.get("rain", {}).get(
            "1h", response_json.get("rain", {}).get("3h", 0.0)),
        "snow": response_json.get("snow", {}).get(
            "1h", response_json.get("snow", {}).get("3h", 0.0)),
        
        "clouds_all": response_json.get("clouds", {}).get("all", 0),
        
        "dt": response_json.get("dt"),
        "dt_text": response_json.get("dt_txt", None),
    }

    return weather_data

def extract_forecast_data(response_json):
    forecast_list = response_json.get("list", [])
    extracted_forecasts = [extract_weather_data(item) for item in forecast_list]
    return extracted_forecasts