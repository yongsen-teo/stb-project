from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Annotated


class ImageData(BaseModel):
    url: Annotated[str, Field(description="Image URL")]
    caption: Annotated[str, Field(description="Image caption (less than 70 words)")]
    hashtags: Annotated[str, Field(description="Hashtags associated with the image")]


class PlaceDetails(BaseModel):
    name: Annotated[str, Field(description="Name of the place")]
    address: Annotated[str, Field(description="Place address")]
    openingHours: Annotated[
        Dict[str, str],
        Field(
            description="Place Opening Hours",
        ),
    ]
    description: Annotated[
        str,
        Field(
            description="Description of the Place",
            min_length=300,
            max_length=400,
        ),
    ]
    topOfferings: Annotated[
        Dict[str, str],
        Field(
            description="Top offerings and prices of the Place",
        ),
    ]
    contactNumber: Annotated[str, Field(description="Contact number of the Place")]
    images: Optional[Dict[str, ImageData]] = None
    citation: Optional[List[str]] = None

    model_config = {
        "extra": "ignore"  # This will ignore any extra fields
    }


class AppResponse(BaseModel):
    status: Annotated[str, Field(description="Status of the response")]
    message: Annotated[str, Field(description="Message of the response")]
    locations: Annotated[
        List[PlaceDetails],
        Field(description="List of Places"),
    ]
    nextPageToken: Optional[
        Annotated[
            str,
            Field(description="Next page token"),
        ]
    ] = None

    model_config = {
        "extra": "ignore"  # This will ignore any extra fields
    }
