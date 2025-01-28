FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use .env file for environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Expose Hugging Face's default port
EXPOSE 7860

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:7860/health || exit 1

# Run the application
CMD uvicorn main:app --host 0.0.0.0 --port 7860 --timeout-keep-alive 30