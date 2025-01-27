import logging
import time
from fastapi import APIRouter, HTTPException

from app.schemas.request import UserRequest
from app.schemas.response import ImageData, PlaceDetails, AppResponse

from app.services.google.places import fetch_places
from app.services.google.photos import get_photo_data

from app.utils.services_formatter import sort_places, format_place_details

from app.llm.generate_place_description import generate_place_description
from app.llm.generate_image_info import generate_image_info
from app.llm.generate_top_offerings import generate_top_offerings

# Set up logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(
    prefix="/locations",
    tags=["Locations"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/search",
    description="Search for locations based on user query",
)
async def search_locations(request: UserRequest) -> AppResponse:
    """Search for locations based on user query."""
    try:
        user_request_body = request.model_dump()
        logger.debug(f"Received user request: {user_request_body}")

        places = fetch_places(user_request_body)
        logger.info(f"Places fetched: {places}")
        logger.info(f"Found {len(places)} raw places results")

        sorted_places = sort_places(places)
        logger.debug(f"Sorted {len(sorted_places)} places")

        locations = []
        for index, place in enumerate(sorted_places, 1):
            try:
                # Format place details
                formatted_place = format_place_details(place)
                logger.debug(f"Format place details: {formatted_place}")

                response_data = formatted_place.get("response_data", {})
                extra_data = formatted_place.get("extra_data", {})

                # Prepare the 'citation' field
                citation = []
                if extra_data.get("websiteUri"):
                    citation.append(extra_data.get("websiteUri", ""))

                # Use 'citation' as per the model
                response_data["citation"] = citation

                place_name = response_data.get("name", "")

                tick = time.time()
                top_offerings = generate_top_offerings(place_name)
                tock = time.time()
                print(f"Generate top_offerings TIME: {tock - tick:.2f} seconds")
                response_data["topOfferings"] = top_offerings

                tick = time.time()
                description = generate_place_description(place_name)
                tock = time.time()
                print(f"Generate description TIME: {tock - tick:.2f} seconds")
                response_data["description"] = description

                # Using extra_data for other logic
                photos = extra_data.get("photos", [])
                if photos:
                    photo_name = photos[0].get("name", "Image")
                    photo_link = photos[0].get("googleMapsUri", "")
                else:
                    logger.warning(f"No photos available for place {place_name}")
                    # Provide default values if no photos are available
                    photo_name = "Default Image"
                    photo_link = "https://example.com/default-image.jpg"

                # Add photo link to 'citation' list
                citation.append(photo_link)
                response_data["citation"] = citation

                photo_data = get_photo_data(
                    photo_name,
                    maxWidthPx=1560,
                    maxHeightPx=878,
                )

                tick = time.time()
                image_body = generate_image_info(photo_data["photo_binary"])
                tock = time.time()
                print(f"Generate image info TIME: {tock - tick:.2f} seconds")

                image_name = image_body.get("name", "Image")
                image_caption = image_body.get("caption", "No caption found")
                image_hashtags = image_body.get("hashtags", "No hashtags found")

                image_data_instance = ImageData(
                    url=photo_link,
                    caption=image_caption,
                    hashtags=image_hashtags,
                )

                # Assign 'images' as a dict with image_name as key
                images = {image_name: image_data_instance}
                response_data["images"] = images

                # Create PlaceDetails instance with correct data
                place_details = PlaceDetails(**response_data)
                locations.append(place_details)

            except Exception as place_error:
                logger.error(
                    f"Error processing place {index}: {str(place_error)}",
                    exc_info=True,
                )
                continue

        logger.info(f"Successfully processed {len(locations)} places")

        app_response = AppResponse(
            status="success",
            message="Places found",
            locations=locations,
        )
        return app_response

    except Exception as e:
        logger.critical("Critical error in locations search", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
