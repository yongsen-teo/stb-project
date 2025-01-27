# Use an official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

# Copy dependency files first to leverage Docker cache
COPY requirements.txt uv.lock pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (uses .dockerignore to exclude unwanted files)
COPY . .

# Expose the port your app runs on (adjust if needed)
EXPOSE 8000

# Command to run the application (adjust if using different ASGI server)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
