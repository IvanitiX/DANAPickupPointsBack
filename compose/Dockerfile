# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get install -y --no-install-recommends netcat-openbsd libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .
COPY requirements-prod.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements-prod.txt

# Copy the project files into the container
COPY src/ .
COPY compose/entrypoint.sh .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["./entrypoint.sh"]