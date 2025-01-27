import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.locations import router as locations_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")],
)

# Disable verbose logging from external libraries
logging.getLogger("google").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.INFO)


# Initialize FastAPI app first
app = FastAPI(
    title="Singapore Attractions API",
    description="Discover locations and events with AI-powered insights",
    version="1.0.0",
)

# Configure CORS before adding routes
# Can add origins to the list when ready for production
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[
    #     "http://localhost",
    #     "http://localhost:3000",
    #     "http://127.0.0.1:3000",
    #     "http://localhost:8000",
    #     # Add production origins here when ready
    # ],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Main API endpoints
app.include_router(
    locations_router,
    prefix="/api/v1",
    tags=["Locations"],
)


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Ping the health of the API"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload
        reload_dirs=["app", "api"],  # Only watch these directories
        reload_includes=["*.py"],  # Only watch Python files
        reload_excludes=["*.log", "*.txt"],  # Ignore these files
        factory=False,
        workers=1,
    )
