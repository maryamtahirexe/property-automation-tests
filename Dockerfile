FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99

# Install dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    xvfb \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="${CHROME_BIN}:${PATH}"

# Copy test files
WORKDIR /tests
COPY . .

# Install Python deps
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Default command to run tests
CMD ["xvfb-run", "--server-args='-screen 0 1024x768x24'", "pytest", "-v", "test_suite.py"]
