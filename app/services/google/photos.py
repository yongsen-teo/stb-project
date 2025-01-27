# import os
import aiohttp
import base64
import requests
import asyncio

from app.config import settings

PLACES_BASE_URL = settings.PLACES_BASE_URL
PLACES_API_KEY = settings.PLACES_API_KEY
FIELDS = settings.PLACES_FIELDS


def get_photo_base64(photo_binary):
    "Converts photo binary to base64"
    photo_base64 = base64.b64encode(photo_binary).decode("utf-8")
    return photo_base64


def get_photo_data(
    photo_name,
    maxWidthPx=1560,
    maxHeightPx=878,
) -> dict:
    """Get photo data from Google Places API"""
    headers = {"X-Goog-Api-Key": PLACES_API_KEY, "Content-Type": "image/jpeg"}
    params = {
        "maxHeightPx": maxHeightPx,
        "maxWidthPx": maxWidthPx,
        "key": PLACES_API_KEY,
    }
    photo_url = f"https://places.googleapis.com/v1/{photo_name}/media"

    try:
        response = requests.get(photo_url, params=params, headers=headers)
        response.raise_for_status()
        if not response.content:
            raise ValueError("Empty response content")
        photo_base64 = get_photo_base64(response.content)
        return {"photo_binary": response.content, "photo_base64": photo_base64}

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"photo_binary": None, "photo_base64": None}

    except Exception as e:
        print(f"Error processing photo: {e}")
        return {"photo_binary": None, "photo_base64": None}


# -- Async version -- #


async def get_photo_data_async(photo_name, maxWidthPx=1560, maxHeightPx=878):
    headers = {"X-Goog-Api-Key": PLACES_API_KEY, "Content-Type": "image/jpeg"}
    params = {
        "maxHeightPx": maxHeightPx,
        "maxWidthPx": maxWidthPx,
        "key": PLACES_API_KEY,
    }
    photo_url = f"https://places.googleapis.com/v1/{photo_name}/media"

    async with aiohttp.ClientSession() as session:
        async with session.get(photo_url, params=params, headers=headers) as response:
            content = await response.read()
            photo_base64 = base64.b64encode(content).decode("utf-8")
            return {"photo_binary": content, "photo_base64": photo_base64}


async def async_get_photos_base64(photos):
    # photo_base64s = []
    photo_binaries = []
    tasks = []

    for photo in photos:
        photo_name = photo.get("name", "")
        tasks.append(get_photo_data_async(photo_name))

    results = await asyncio.gather(*tasks)
    for result in results:
        if result:
            # photo_base64s.append(result["photo_base64"])
            photo_binaries.append(result["photo_binary"])

    assert len(photo_binaries) == len(photos), "Mismatch in number of photos"

    # return photo_base64s
    return photo_binaries


# Wrapper if you need to call it from sync code
def get_photos_base64_sync(photos):
    return asyncio.run(async_get_photos_base64(photos))


# --- In case you want to save the photo --- #


def save_photo_jpeg(photo_binary, filename):
    with open(f"./{filename}.jpeg", "wb") as f:
        f.write(photo_binary)
        print(f"Saved {filename}.jpeg")
