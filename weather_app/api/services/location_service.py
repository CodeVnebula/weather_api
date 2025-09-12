import os
import requests

from api.config.endpoints import ENDPOINTS
from api.config.settings import LOCATION_LIMIT

def fetch_locations_from_api(city_name, state_code="", country_code=""):
    api_key = os.getenv("WEATHERMAP_API_KEY")
    url = (
        f"{ENDPOINTS['geocoding']}?"
        f"q={city_name},{state_code},{country_code}"
        f"&limit={LOCATION_LIMIT}&appid={api_key}"
    )
    return requests.get(url)


def clean_location_results(response_json):
    for location in response_json:
        location.pop("local_names", None)

    seen = set()
    unique = []
    for location in response_json:
        identifier = (
            location["name"], location.get("state"), location["country"]
        )
        if identifier not in seen:
            seen.add(identifier)
            unique.append(location)

    return unique

def extract_location_data(
        response_json, state=None, precise_name=None, population=0
    ):
    # Extracting location from "city" dict if it exists
    location_json = response_json.get("city", response_json)

    # Determine population: if location_json population is 
    # 0 and parameter population is not 0, use parameter
    loc_population = location_json.get("population", 0)
    if loc_population == 0 and population != 0:
        final_population = population
    else:
        final_population = loc_population

    location_data = {
        "name": location_json.get("name"),
        "precise_name": precise_name.strip() if precise_name else None,
        "state": state.strip() if state else None,
        "lat": location_json.get("coord", {}).get("lat"),
        "lon": location_json.get("coord", {}).get("lon"),
        "country": location_json.get("country")
        or location_json.get("sys", {}).get("country", ""),
        "population": final_population,
        "timezone": location_json.get("timezone"),
        "sunrise": location_json.get("sunrise")
        or location_json.get("sys", {}).get("sunrise"),
        "sunset": location_json.get("sunset")
        or location_json.get("sys", {}).get("sunset"),
    }

    return location_data
