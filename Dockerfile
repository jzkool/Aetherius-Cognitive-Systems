# Use official Python 3.11 slim image as the base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for scientific libraries like scipy and jax
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the standard Gradio port (Hugging Face Spaces defaults to 7860)
EXPOSE 7860
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "app.py"]
