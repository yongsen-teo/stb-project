# app/config.py
import os
from typing import List
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))


class Config:
    PLACES_API_KEY = os.environ.get("PLACES_API_KEY")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    PLACES_BASE_URL = "https://places.googleapis.com/v1/places"

    LANGUAGE_CODE: str = "en"
    REGION_CODE: str = "SG"

    # Fields
    PLACES_FIELDS: List[str] = [
        "places.id",
        "places.displayName",
        "places.types",
        "places.formattedAddress",
        "places.internationalPhoneNumber",
        "places.currentOpeningHours.weekdayDescriptions",
        "places.regularOpeningHours.weekdayDescriptions",
        "places.priceRange",
        "places.priceLevel",
        "places.rating",
        "places.userRatingCount",
        # "places.editorialSummary",
        # "places.reviews.text.text",
        "places.photos.name",
        "places.photos.googleMapsUri",
        "places.websiteUri",
    ]


settings = Config()
