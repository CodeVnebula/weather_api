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
