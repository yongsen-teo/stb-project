from pydantic import BaseModel, Field
from typing import List, Optional, Annotated


class UserRequest(BaseModel):
    user_query: Annotated[
        str,
        Field(
            description="User query string",
            min_length=5,
            max_length=50,
        ),
    ]
    page_size: Optional[
        Annotated[
            int,
            Field(
                description="Number of results to return",
                gt=0,
                lt=20,
            ),
        ]
    ] = 5
    extra_fields: Optional[
        Annotated[
            Optional[List[str]],
            Field(
                description="Extra fields to include in response",
            ),
        ]
    ] = []
    nextPageToken: Optional[
        Annotated[
            (str),
            Field(description="Next page token"),
        ]
    ] = None
