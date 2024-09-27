# Dockerfile

# Use official Python image as the base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install PDM
RUN pip install pdm

# Copy pyproject.toml and pdm.lock
COPY pyproject.toml pdm.lock* /app/

# Install dependencies
RUN pdm install --prod

# Copy the rest of the application code
COPY src/ /app/src/
COPY predefined_data.json /app/predefined_data.json

# Expose the port
EXPOSE 7860

# Set environment variables for OpenAI API key (should be overridden in deployment)
ENV OPENAI_API_KEY=""

# Run the application
CMD ["pdm", "run", "start"]
