# Project Name

## Quick Start

1. Clone this repository
2. Run `docker compose up`
3. Visit `http://localhost:8000`

## Environment Variables

Create a `.env` file with:

- GEMINI_API_KEY = "your google genai gemini api key"
- PLACES_API_KEY = "your google places (v2) api key"

Detailed explanation:

### Method 1

1. Create a Google Cloud Project, set up billing and create a new API key
2. Attach the Places API (new) and the Generative Language API to your API key
3. This allows you to use one single API for both Google resources.

### Method 2

1. Repeat the same process and create a API key just for Google Places API
   (new).
2. Go to the Google AIStudio page to generate a Gemini API key.
   [https://aistudio.google.com/apikey]
3. Parse both keys for your .env variables.

## Requirements

- Google Cloud Project and billing account
- Docker
- Docker Compose
