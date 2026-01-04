# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Enable multi-arch support and install Google Chrome
RUN dpkg --add-architecture amd64 \
    && mkdir -p /etc/apt/keyrings \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y \
        google-chrome-stable:amd64 \
        libasound2:amd64 \
        libatk-bridge2.0-0:amd64 \
        libatk1.0-0:amd64 \
        libatspi2.0-0:amd64 \
        libc6:amd64 \
        libcairo2:amd64 \
        libcups2:amd64 \
        libcurl4:amd64 \
        libdbus-1-3:amd64 \
        libexpat1:amd64 \
        libgbm1:amd64 \
        libglib2.0-0:amd64 \
        libgtk-3-0:amd64 \
        libnspr4:amd64 \
        libnss3:amd64 \
        libpango-1.0-0:amd64 \
        libudev1:amd64 \
        libvulkan1:amd64 \
        libx11-6:amd64 \
        libxcb1:amd64 \
        libxcomposite1:amd64 \
        libxdamage1:amd64 \
        libxext6:amd64 \
        libxfixes3:amd64 \
        libxkbcommon0:amd64 \
        libxrandr2:amd64 \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
# Get Chrome version and download matching ChromeDriver
# Install jq for JSON parsing
RUN apt-get update && apt-get install -y jq && rm -rf /var/lib/apt/lists/*

RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1) \
    && echo "Installed Chrome version: $CHROME_VERSION" \
    && echo "Attempting to download matching ChromeDriver..." \
    && CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | jq -r '.channels.Stable.version' 2>/dev/null) \
    && if [ -z "$CHROMEDRIVER_VERSION" ] || [ "$CHROMEDRIVER_VERSION" = "null" ]; then \
        echo "API lookup failed, searching for version matching Chrome ${CHROME_MAJOR_VERSION}..."; \
        CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json" | jq -r "[.versions[] | select(.version | startswith(\"${CHROME_MAJOR_VERSION}.\")) | .version] | .[-1]" 2>/dev/null); \
    fi \
    && if [ -z "$CHROMEDRIVER_VERSION" ] || [ "$CHROMEDRIVER_VERSION" = "null" ]; then \
        echo "Using installed Chrome version as ChromeDriver version: $CHROME_VERSION"; \
        CHROMEDRIVER_VERSION="$CHROME_VERSION"; \
    fi \
    && echo "Downloading ChromeDriver version: $CHROMEDRIVER_VERSION" \
    && wget -q -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" \
    && if [ ! -s /tmp/chromedriver.zip ]; then \
        echo "Download failed, verifying ChromeDriver version exists..."; \
        exit 1; \
    fi \
    && unzip -q /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 \
    && chmod +x /usr/local/bin/chromedriver \
    && echo "ChromeDriver installed successfully:" \
    && chromedriver --version

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY .env* ./

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

