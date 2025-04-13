# Advanced Web Scraper

A dockerized web scraping application with multiple scraping methods including requests, Selenium, stealth Selenium, and Nodriver.

## Features

- Multiple scraping methods in one tool
- Proxy support
- User-agent rotation
- IP verification
- HTML content saving

## Requirements

- Docker
- Docker Compose

## Setup and Usage

1. Clone this repository
2. Navigate to the project directory
3. Build and run the Docker container:

```bash
docker-compose build
docker-compose up
```

### Command Line Options

You can pass command line arguments through docker-compose:

```bash
# Run with a specific method
docker-compose run scraper --method requests

# Run with a proxy
docker-compose run scraper --method all --proxy host:port:username:password

# Available methods:
# - all: Run all methods
# - requests: Use Python requests
# - selenium: Use Selenium WebDriver
# - stealth: Use Stealth Selenium
# - nodriver: Use Nodriver
```

## Output

The scraped HTML files will be saved in folders named after the target domain. Each file is prefixed with the scraping method used and a timestamp.

## Notes

- The Headless Chrome browser runs inside the Docker container
- The application checks your IP via ipchicken.com before visiting the target site
- Make sure your proxy is working if you're using one