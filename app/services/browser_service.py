import asyncio
import random
from typing import Optional, Tuple
from playwright.async_api import async_playwright, Page, Browser

# User-Agent list for basic rotation to avoid simple bot detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
]

async def scrape_product_page(url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Scrapes the content of a product page using Playwright.
    
    Args:
        url (str): The URL of the product page to scrape.
        
    Returns:
        Tuple[Optional[str], Optional[str]]: (content, error_message).
        If success: (content, None).
        If failure: (None, error_message).
    """
    async with async_playwright() as p:
        # Launch browser in headless mode with extra args to try and look more "human"
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        
        # Create a new context with a random User-Agent and extra headers
        user_agent = random.choice(USER_AGENTS)
        context = await browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1,
            locale="en-US,en;q=0.9",
        )
        
        page = await context.new_page()
        
        # Add extra headers
        await page.set_extra_http_headers({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
        })
        
        try:
            print(f"Navigating to {url}...")
            # Navigate to the URL and wait for network to be idle
            # Increased timeout to 90s just in case
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            
            # Wait a bit for dynamic content to settle
            await page.wait_for_timeout(3000)
            
            # Check if we got blocked (simple check for common block texts)
            # Refined to be less aggressive - only check title or very short content
            content_length = len(await page.content())
            title = await page.title()
            
            if "captcha" in title.lower() or "bot" in title.lower() and "robot" not in title.lower(): # Avoid matching "Robot Vacuum"
                 return None, f"Bot detection triggered (Title: {title})"

            # Extract the visible text
            body_text = await page.evaluate("document.body.innerText")
            
            if not body_text or len(body_text) < 200:
                 return None, "Page loaded but content seems empty or too short (potential block)."
            
            full_content = f"Title: {title}\n\nContent:\n{body_text}"
            
            return full_content, None
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error scraping {url}: {error_msg}")
            return None, f"Scraping failed: {error_msg}"
            
        finally:
            await browser.close()

if __name__ == "__main__":
    # Test the scraper independently
    test_url = "https://www.example.com"
    content, error = asyncio.run(scrape_product_page(test_url))
    if error:
        print(f"Failed: {error}")
    else:
        print(content[:500] + "...")
