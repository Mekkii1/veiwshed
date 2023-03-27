# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the source code into the container
COPY . .

# Install the dependencies
RUN pip install geopy mgrs fastapi uvicorn pydantic

# Expose the port that the API will run on
EXPOSE 8000

# Start the API with Uvicorn
CMD ["uvicorn", "destination-point-api:app", "--host", "127.0.0.1", "--port", "8000"]
