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
3. Run server

### Command Line Options

```bash
# Run server
uvicorn server:app --reload --host 127.0.0.1 --port 6024

```bash
# Run dev server
uvicorn server:app --reload

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