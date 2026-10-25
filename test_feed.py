import asyncio
import json
from playwright.async_api import async_playwright

async def run():
    with open(r"D:\Projects\linkedin-agent-studio\linkedin_user_data\session_cookies.json") as f:
        cookies = json.load(f)

    # Sanitize JSESSIONID value
    clean_cookies = []
    for c in cookies:
        c_copy = dict(c)
        if c_copy["name"] == "JSESSIONID":
            c_copy["value"] = c_copy["value"].strip('"').strip("'")
        clean_cookies.append(c_copy)

    # Add required companion cookies
    clean_cookies.append({"name": "bcookie", "value": "v=2&791b5c49-8041-4770-96f3", "domain": ".linkedin.com", "path": "/"})
    clean_cookies.append({"name": "bscookie", "value": "v=1&20261025185347", "domain": ".linkedin.com", "path": "/"})
    clean_cookies.append({"name": "lang", "value": "v=2&lang=en-us", "domain": ".linkedin.com", "path": "/"})

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        await context.add_cookies(clean_cookies)
        page = await context.new_page()

        print("Navigating to LinkedIn Feed...")
        await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
        await asyncio.sleep(4)
        print("Page URL:", page.url)
        print("Page Title:", await page.title())
        
        # Check start post button
        btn = page.locator("button:has-text('Start a post')").first
        print("Start post visible:", await btn.is_visible())
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
