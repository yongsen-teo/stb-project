# Project Name: STB Places Finder

- for project documentation, **PLEASE REFER** to the README link below:
  [PROJECT_README.md]

- this page will mainly cover the setting up of the project and API keys

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

1. Create a Google Cloud Project, set up billing account and create a new API key.
   Link is [https://console.cloud.google.com/apis]
2. Attach the Places API (new) and the Generative Language API to your
   credentials key.
   [demo pic](google_cloud_api_keys.jpg)
3. This allows you to use one single API key for both Google resources.
4. Your `.env` file will hence be:

```
GEMINI_API_KEY="your single API key"
PLACES_API_KEY="your single API key"
```

### Method 2

1. Repeat the same process and create a API key just for Google Places API
   (new).
2. Go to the Google AIStudio page to generate a Gemini API key.
   [https://aistudio.google.com/apikey]
3. Parse both keys for your .env variables.

```
GEMINI_API_KEY="your gemini api key"
PLACES_API_KEY="your google places api key"
```

## Requirements

- Google Cloud Project and billing account
- Docker
- Docker Compose
