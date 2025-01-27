# STB Project Writeup

## Main use

- user sends a query asking about locations and events in SG
- REST API will process the query and return structured data

## Main tools used

### Google Places V2 API

- Google Places (V2) API as its searchText endpoint enables a direct search on local companies information

### Gemini as LLM provider

- Allows integration with Places API
- Decent, cheap and fast performance.

## Data Flow

- User sends a POST request to the endpoint http://0.0.0.0:8000/api/v1/locations/search

- App directs to location router endpoint and call the Google Places API
- Page size set at default of 5 and photo limit set as default of 1 per location.
- Lowers latency, costs and bandwidth usage by removing non-needed fields.

- Places API response is a list of places with attributes
- App will take some and format accordingly to requirement, and use other fields for content generation.
- RatingWeight to sort places (rating x ratingCount)
- More relevant and engaging results will be top on the list hence.
- Some formatting functions used for some fields (opening hours, phone number etc)

- Places attribute will have Photo name, which can be used to call the Photos API.
- Photos API returns the content of the image and this can be used for image captioning.

### LLM models

- place description model which uses STB website examples for tonality matching (few shot prompts)
- Top offering model that returns the top offerings of the restaurant and its estimated price too
- multimodal Gemini LLM that takes in images and generates its name, caption and potential hashtags.
- LLM were using Gemini 2.0 Flash Expt with few shot prompting.

### Response

- consolidate all the data (including generated ones) and provide the Response body for the user.

## Main issues

- currently the code is running the image caption and other LLMs synchronously and I have plans to make it asynchronous for production use
- The search results accuracy can be better, by perhaps including the other fields so maybe an LLM can filter the places list better

## Moving forward

- Async for long processing tasks
- LLM prompt templates can be stored in DB
- Use S3 to store images and to read and write them
