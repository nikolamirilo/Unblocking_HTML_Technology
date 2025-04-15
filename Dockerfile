FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose port (if you're using a web server – not needed for pure scraping scripts)
EXPOSE 6024

# Run your script
CMD ["python", "main.py"]
# Install Chrome and required dependencies
# RUN apt-get update && apt-get install -y \
#     wget \
#     gnupg \
#     unzip \
#     xvfb \
#     libxi6 \
#     libgconf-2-4 \
#     default-jdk \
#     libglib2.0-0 \
#     libnss3 \
#     libgbm1 \
#     libasound2 \
#     libxss1 \
#     fonts-liberation \
#     libappindicator3-1 \
#     libatk-bridge2.0-0 \
#     libatk1.0-0 \
#     libcups2 \
#     libdbus-1-3 \
#     libxcomposite1 \
#     libxdamage1 \
#     libxfixes3 \
#     libxrandr2 \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Install Chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
#     && apt-get update \
#     && apt-get install -y google-chrome-stable \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Install Chrome WebDriver
# RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1-3) \
#     && CHROME_DRIVER_VERSION=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") \
#     && wget -q "https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip" \
#     && unzip chromedriver_linux64.zip \
#     && mv chromedriver /usr/bin/chromedriver \
#     && chmod +x /usr/bin/chromedriver \
#     && rm chromedriver_linux64.zip

# # Copy requirements file
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the application code
# COPY . .

# EXPOSE 6024
# # Command to run the scraper with all methods by default
# ENTRYPOINT ["python", "-m", "asyncio", "main.py"]
# CMD ["--method", "all"]