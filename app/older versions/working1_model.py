import requests
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Removed undetected_chromedriver import
from bs4 import BeautifulSoup
import argparse
import os

# Check if nodriver is available, if not provide instructions
try:
    import nodriver
    NODRIVER_AVAILABLE = True
except ImportError:
    NODRIVER_AVAILABLE = False

class ZooplaScraper:
    def __init__(self, proxy=None):
        self.url = "https://clinicaltrials.gov/study/NCT03054870?cond=pulmonary&rank=1"
        self.ip_check_url = "https://ipchicken.com/"
        self.proxy = proxy
        
    def get_random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:91.0) Gecko/20100101 Firefox/91.0"
        ]
        return random.choice(user_agents)
    
    def format_proxy(self):
        """Format proxy string for different libraries"""
        if not self.proxy:
            return None
            
        # Extract components from proxy string (assuming format: host:port or host:port:user:pass)
        parts = self.proxy.split(':')
        if len(parts) == 2:  # host:port format
            host, port = parts
            return {
                'requests': f"http://{host}:{port}",
                'selenium': f"{host}:{port}",
                'selenium_dict': {
                    'proxy': {
                        'http': f"http://{host}:{port}",
                        'https': f"https://{host}:{port}",
                    }
                }
            }
        elif len(parts) == 4:  # host:port:user:pass format
            host, port, user, password = parts
            return {
                'requests': f"http://{user}:{password}@{host}:{port}",
                'selenium': f"{host}:{port}:{user}:{password}",
                'selenium_dict': {
                    'proxy': {
                        'http': f"http://{user}:{password}@{host}:{port}",
                        'https': f"https://{user}:{password}@{host}:{port}",
                    }
                }
            }
        else:
            raise ValueError("Invalid proxy format. Use host:port or host:port:user:pass")
    
    def save_html(self, html, method):
        """Save the HTML content to a file"""
        filename = f"zoopla_{method}_{int(time.time())}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"HTML saved to {filename}")
        return filename
        
    def extract_ip_from_ipchicken(self, html):
        """Extract IP address from IPChicken HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        # IPChicken typically shows the IP in the first large text block
        ip_text = soup.get_text()
        import re
        ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        match = re.search(ip_pattern, ip_text)
        if match:
            return match.group(0)
        return "IP not found"
        
    def scrape_with_requests(self):
        """Scrape using Python requests with proxy"""
        print("\n=== Scraping with Python Requests ===")
        
        proxies = None
        if self.proxy:
            proxy_format = self.format_proxy()
            proxies = {
                'http': proxy_format['requests'],
                'https': proxy_format['requests']
            }
            print(f"Using proxy: {proxies}")
        
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        
        # First check IP with IPChicken
        try:
            ip_response = requests.get(self.ip_check_url, headers=headers, proxies=proxies, timeout=30)
            ip_html = ip_response.text
            ip_address = self.extract_ip_from_ipchicken(ip_html)
            print(f"IP Address (via IPChicken): {ip_address}")
            
            # Now scrape Zoopla
            response = requests.get(self.url, headers=headers, proxies=proxies, timeout=30)
            html = response.text
            
            # Save HTML to file
            filename = self.save_html(html, "requests")
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Size: {len(html)} bytes")
            
            return html
        except Exception as e:
            print(f"Error with requests method: {str(e)}")
            return None

    def scrape_with_selenium(self):
        """Scrape using Selenium with Chrome and proxy"""
        print("\n=== Scraping with Selenium Chrome ===")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-agent={self.get_random_user_agent()}")
        
        # Add proxy if provided
        if self.proxy:
            proxy_format = self.format_proxy()
            chrome_options.add_argument(f'--proxy-server={proxy_format["selenium"]}')
            print(f"Using proxy: {proxy_format['selenium']}")
        
        try:
            # Initialize the Chrome driver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            
            # First check IP with IPChicken
            driver.get(self.ip_check_url)
            time.sleep(3)  # Wait for page to load
            ip_html = driver.page_source
            ip_address = self.extract_ip_from_ipchicken(ip_html)
            print(f"IP Address (via IPChicken): {ip_address}")
            
            # Now scrape Zoopla
            driver.get(self.url)
            
            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get the page source
            html = driver.page_source
            
            # Save HTML to file
            filename = self.save_html(html, "selenium")
            
            print(f"Response Size: {len(html)} bytes")
            
            driver.quit()
            return html
        except Exception as e:
            print(f"Error with Selenium method: {str(e)}")
            return None

    def scrape_with_stealth_selenium(self):
        """Scrape using Selenium with enhanced stealth features (alternative to undetected-chromedriver)"""
        print("\n=== Scraping with Stealth Selenium ===")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(f"--user-agent={self.get_random_user_agent()}")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Add proxy if provided
        if self.proxy:
            proxy_format = self.format_proxy()
            chrome_options.add_argument(f'--proxy-server={proxy_format["selenium"]}')
            print(f"Using proxy: {proxy_format['selenium']}")
        
        try:
            # Initialize the Chrome driver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            
            # Execute CDP commands to make navigator.webdriver undefined
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """
            })
            
            # First check IP with IPChicken
            driver.get(self.ip_check_url)
            time.sleep(3)  # Wait for page to load
            ip_html = driver.page_source
            ip_address = self.extract_ip_from_ipchicken(ip_html)
            print(f"IP Address (via IPChicken): {ip_address}")
            
            # Now scrape Zoopla
            driver.get(self.url)
            time.sleep(5)  # Wait for dynamic content to load
            
            # Add random mouse movements and scrolling to mimic human behavior
            driver.execute_script("""
                // Random scroll
                window.scrollTo(0, Math.floor(Math.random() * 100));
                window.scrollTo(0, Math.floor(Math.random() * 300));
            """)
            time.sleep(random.uniform(2, 4))
            
            # Get the page source
            html = driver.page_source
            
            # Save HTML to file
            filename = self.save_html(html, "stealth_selenium")
            
            print(f"Response Size: {len(html)} bytes")
            
            driver.quit()
            return html
        except Exception as e:
            print(f"Error with Stealth Selenium method: {str(e)}")
            return None

    def scrape_with_nodriver(self):
        """Scrape using Nodriver with proxy"""
        if not NODRIVER_AVAILABLE:
            print("\n=== Nodriver module not available ===")
            print("Please install it with: pip install nodriver")
            return None
            
        print("\n=== Scraping with Nodriver ===")
        
        try:
            proxy_url = None
            if self.proxy:
                proxy_format = self.format_proxy()
                proxy_url = proxy_format['requests']
                print(f"Using proxy: {proxy_url}")
            
            # Create a nodriver session
            session = nodriver.Session()
            
            # Set proxy if provided
            if proxy_url:
                session.proxies = {"http": proxy_url, "https": proxy_url}
            
            # Set user agent
            session.headers.update({"User-Agent": self.get_random_user_agent()})
            
            # First check IP with IPChicken
            ip_response = session.get(self.ip_check_url)
            ip_html = ip_response.text
            ip_address = self.extract_ip_from_ipchicken(ip_html)
            print(f"IP Address (via IPChicken): {ip_address}")
            
            # Now scrape Zoopla
            response = session.get(self.url)
            html = response.text
            
            # Save HTML to file
            filename = self.save_html(html, "nodriver")
            
            print(f"Response Size: {len(html)} bytes")
            
            return html
        except Exception as e:
            print(f"Error with Nodriver method: {str(e)}")
            return None

def main():
    parser = argparse.ArgumentParser(description='Zoopla Scraper with various methods')
    parser.add_argument('--proxy', help='Proxy in format host:port or host:port:username:password', default=None)
    parser.add_argument('--method', choices=['all', 'requests', 'selenium', 'stealth', 'nodriver'], 
                        default='all', help='Scraping method to use')
    
    args = parser.parse_args()
    
    # Create scraper instance
    scraper = ZooplaScraper(proxy=args.proxy)
    
    results = {}
    
    if args.method in ['all', 'requests']:
        results['requests'] = scraper.scrape_with_requests()
        
    if args.method in ['all', 'selenium']:
        results['selenium'] = scraper.scrape_with_selenium()
        
    if args.method in ['all', 'stealth']:
        results['stealth'] = scraper.scrape_with_stealth_selenium()
        
    if args.method in ['all', 'nodriver']:
        results['nodriver'] = scraper.scrape_with_nodriver()
    
    # Print summary
    print("\n=== Scraping Summary ===")
    for method, html in results.items():
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string if soup.title else "No title found"
            print(f"{method}: Success - {title} ({len(html)} bytes)")
        else:
            print(f"{method}: Failed")

if __name__ == "__main__":
    main()