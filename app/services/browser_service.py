import asyncio
import random
from typing import Optional
from playwright.async_api import async_playwright, Page, Browser

# User-Agent list for basic rotation to avoid simple bot detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
]

async def scrape_product_page(url: str) -> Optional[str]:
    """
    Scrapes the content of a product page using Playwright.
    
    Args:
        url (str): The URL of the product page to scrape.
        
    Returns:
        Optional[str]: The text content of the page, or None if scraping failed.
    """
    async with async_playwright() as p:
        # Launch browser in headless mode
        browser = await p.chromium.launch(headless=True)
        
        # Create a new context with a random User-Agent
        user_agent = random.choice(USER_AGENTS)
        context = await browser.new_context(user_agent=user_agent)
        
        page = await context.new_page()
        
        try:
            print(f"Navigating to {url}...")
            # Navigate to the URL and wait for network to be idle
            # This ensures that dynamic content has likely loaded
            await page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Extract the relevant content
            # We'll take the 'body' text which usually contains the visible product info
            # For more complex sites, we might need specific selectors, but body is a good general catch-all for LLM processing
            content = await page.evaluate("document.body.innerText")
            
            # Also get the title just in case
            title = await page.title()
            
            # Combine title and content
            full_content = f"Title: {title}\n\nContent:\n{content}"
            
            return full_content
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
            
        finally:
            await browser.close()

if __name__ == "__main__":
    # Test the scraper independently
    test_url = "https://www.example.com"
    result = asyncio.run(scrape_product_page(test_url))
    print(result[:500] + "..." if result else "Failed to scrape")
