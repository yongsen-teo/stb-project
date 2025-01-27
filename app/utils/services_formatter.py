import re
import logging
from datetime import datetime
from typing import List, Dict, Any


def sort_places(places: List) -> List:
    """
    Sort places by
    - rating Weight = userRating * userRatingCount
    """

    def calculate_rating_weight(place):
        rating = place.get("rating", 0)
        count = place.get("userRatingCount", 0)
        return rating * count

    # Sort in descending order (highest weight first)
    sorted_places = sorted(
        places,
        key=calculate_rating_weight,
        reverse=True,
    )
    return sorted_places


def format_contact_number(contact_number: str) -> str:
    "Convert '+65 9456 7890' to '+65-9456-7890' format"
    return contact_number.replace(" ", "-")


def to_military(time_str):
    """Convert 12-hour time to military time."""
    if time_str.lower() == "closed":
        return "Closed"

    # Remove any unicode dashes and standardize format
    time_str = re.sub(r"[–—]", "-", time_str)
    time_str = re.sub(r"\s*-\s*", "-", time_str)

    # Handle multiple time ranges
    if "," in time_str:
        ranges = time_str.split(",")
        return ", ".join(to_military(r.strip()) for r in ranges)

    try:
        start, end = time_str.split("-")
        start = start.strip()
        end = end.strip()

        # Add missing AM/PM to start time based on end time
        if "M" not in start.upper():
            end_period = re.search(r"[AP]M", end, re.I).group()
            start = f"{start} {end_period}"

        # Parse and convert times
        parse_time = lambda t: datetime.strptime(t.strip(), "%I:%M %p").strftime("%H%M")
        return f"{parse_time(start)}-{parse_time(end)}"
    except Exception as e:
        return f"Error: {time_str}"


def format_opening_hours(schedule_list):
    """Format a list of daily schedules to military time."""
    formatted = []
    cleaned_schedules = {}

    for schedule in schedule_list:
        day, hours = schedule.split(": ", 1)
        military_time = to_military(hours)
        formatted.append(f"{day}: {military_time}")

    for result in formatted:
        day, time = result.split("day: ", 1)
        day = day[:3]
        cleaned_schedules[day] = time

    return cleaned_schedules


def format_price_range_with_currency(priceRange: dict) -> str:
    """Convert priceRange to 'SGD $ startPrice-endPrice'"""
    start = priceRange.get("startPrice", {}).get("units", "")
    end = priceRange.get("endPrice", {}).get("units", "")
    currency = priceRange.get("startPrice", {}).get("currencyCode", "")

    return f"{currency} ${start}-{end}"


def format_place_details(place_data: Dict[Any, Any]) -> dict:
    """Format raw place data into dictionary model."""

    logging.debug(f"Formatting place data: {place_data}")
    print(f"Formatting place data: {place_data}")

    opening_hours = place_data.get("currentOpeningHours", {}).get(
        "weekdayDescriptions", []
    )
    print(f"Raw opening hours: {opening_hours}")

    openingHours = format_opening_hours(opening_hours)
    print(f"Opening hours: {openingHours}")

    contactNumber = place_data.get("internationalPhoneNumber", "")
    contactNumber = format_contact_number(contactNumber)
    name = place_data.get("displayName", "")
    name = name.get("text", "")
    address = place_data.get("formattedAddress", "")

    response_data = {
        "name": name,
        "address": address,
        "openingHours": openingHours,
        "contactNumber": contactNumber,
        "description": "",
        "citation": [],
    }

    types = place_data.get("types", "")
    priceRange = place_data.get("priceRange", {})
    if priceRange == {}:
        priceRange = "Please check the website for more information."
    else:
        priceRange = format_price_range_with_currency(priceRange)

    reviews = place_data.get("reviews", [])
    photos = place_data.get("photos", [])
    editiorialSummary = place_data.get("editiorialSummary", "")
    website_uri = place_data.get("websiteUri", "")

    extra_data = {
        "types": types,
        "priceRange": priceRange,
        "reviews": reviews,
        "photos": photos,
        "editorialSummary": editiorialSummary,
        "websiteUri": website_uri,
    }

    # Combine response_data and extra_data

    formatted_data = {
        "response_data": response_data,
        "extra_data": extra_data,
    }
    return formatted_data
