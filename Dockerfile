FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget unzip curl gnupg && \
    apt-get install -y xvfb && \
    apt-get install -y libnss3 libgconf-2-4 libxi6 libxcursor1 libxcomposite1 libasound2 libxdamage1 libxrandr2 libgl1-mesa-glx libgtk-3-0

# Install Chrome
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Set display port to avoid crash
ENV DISPLAY=:99

# Set work directory
WORKDIR /tests

# Copy files
COPY . .

# Install Python packages
RUN pip install -r requirements.txt

# Entry point
CMD ["bash", "run_tests.sh"]
