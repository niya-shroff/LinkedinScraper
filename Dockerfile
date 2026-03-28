# --------------------------
# Base image
# --------------------------
FROM python:3.11-slim

# --------------------------
# Set working directory
# --------------------------
WORKDIR /app

# --------------------------
# Install system dependencies and Chromium
# --------------------------
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    curl \
    unzip \
    jq \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# --------------------------
# Set environment variables for undetected-chromedriver
# --------------------------
ENV CHROMEDRIVER_PATH=/usr/lib/chromium/chromedriver
ENV GOOGLE_CHROME_BIN=/usr/bin/chromium
ENV PYTHONUNBUFFERED=1

# --------------------------
# Copy Python requirements and install
# --------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --------------------------
# Copy application code
# --------------------------
COPY backend/ ./backend/
COPY .env* ./

# --------------------------
# Expose port
# --------------------------
EXPOSE 8000

# --------------------------
# Run the FastAPI app
# --------------------------
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]