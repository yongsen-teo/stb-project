# app/services/google/places.py
import requests
from app.config import settings

BASE_URL = settings.PLACES_BASE_URL
PLACES_API_KEY = settings.PLACES_API_KEY
FIELDS = settings.PLACES_FIELDS
GEMINI_API_KEY = settings.GEMINI_API_KEY


def fetch_places(request: dict, fields: list[str] = FIELDS) -> list:
    """
    Calls Google Places (v2) API to get places based on user query.
    Includes fields specified in the fields parameter.

    Args:
    - user_query (str): User query to search for places
    - fields (list): List of fields to include in the response

    Returns:
    - places (list): List of places
    """
    user_query = request.get("user_query", "")
    page_size = request.get("page_size", 5)
    extra_fields = request.get("extra_fields", [])
    next_page_token = request.get("next_page_token", "")

    fields = fields + extra_fields

    search_places_url = "https://places.googleapis.com/v1/places:searchText"
    print(f"Fetching places from: {search_places_url}")

    headers = {
        "X-Goog-Api-Key": PLACES_API_KEY,
        "X-Goog-FieldMask": ",".join(fields) if fields else "*",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "textQuery": user_query,
        "pageSize": page_size,
        "pageToken": next_page_token,
        "languageCode": "en",
        "regionCode": "sg",
    }
    response = requests.post(
        search_places_url,
        json=payload,
        headers=headers,
    )
    print(f"Fetch Places Response: {response}")
    response.encoding = "utf-8"
    response = response.json()
    places = response.get("places", [])
    print(f"Places API {response}")

    # Limit no. of photos and reviews to 1 each
    for place in places:
        place["photos"] = place.get("photos", [])[:1]
        place["reviews"] = place.get("reviews", [])[:1]

    return places
