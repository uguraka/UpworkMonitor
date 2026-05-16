FROM python:3.12-slim

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install prerequisites, Chrome, and Cloudflare-bypass dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    xvfb \
    xdotool \
    ca-certificates \
    python3-tk \
    python3-dev \
    fonts-liberation \
    fonts-dejavu \
    fonts-noto \
    xfonts-100dpi \
    xfonts-75dpi \
    xfonts-cyrillic \
    libgbm1 \
    libnss3 \
    libvulkan1 \
    tzdata \
    --no-install-recommends \
    && wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y /tmp/chrome.deb \
    && rm /tmp/chrome.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source files
COPY main.py upwork_scraper.py telegram_bot.py entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
