from fastapi import FastAPI
from scraper import AdvancedScraper 

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Scraper API is running"}

@app.get("/scrape")
async def scrape(method: str = "all", proxy: str = None):
    scraper = AdvancedScraper(proxy=proxy)
    results = {} 

    if method in ['all', 'requests']:
        results['requests'] = scraper.scrape_with_requests()

    if method in ['all', 'selenium']:
        results['selenium'] = scraper.scrape_with_selenium()

    if method in ['all', 'stealth']:
        results['stealth'] = scraper.scrape_with_stealth_selenium()

    if method in ['all', 'nodriver']:
        results['nodriver'] = await scraper.scrape_with_nodriver()

    return {k: ("Success" if v else "Failed") for k, v in results.items()}
