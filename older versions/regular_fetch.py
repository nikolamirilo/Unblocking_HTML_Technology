from playwright.sync_api import sync_playwright

def fetch_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Use headless=False for debugging
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()

        print("Opening page...")
        try:
            page.goto(url, timeout=90000)  # Increased timeout
            page.wait_for_load_state("networkidle")

            # Extra delay to ensure JavaScript rendering
            page.wait_for_timeout(7000)  # Adjust if needed

            # Scroll to bottom to load all elements (for infinite scrolling)
            for _ in range(5):  
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                page.wait_for_timeout(2000)

            # Wait for specific content
            try:
                page.wait_for_selector(".css-1itfubx", timeout=15000)  
            except:
                print("Warning: Target element not found, continuing...")

            html = page.content()

            # Save HTML to file
            with open("output.html", "w", encoding="utf-8") as file:
                file.write(html)

            print("HTML saved successfully!")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            browser.close()

fetch_html("https://www.zoopla.co.uk/to-rent/property/london/?price_frequency=per_month&q=London&search_source=to-rent")
