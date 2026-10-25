import asyncio
import os
import json
import sys

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from playwright.async_api import async_playwright

USER_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "linkedin_user_data"))
COOKIE_FILE = os.path.join(USER_DATA_DIR, "session_cookies.json")

async def main():
    print("=" * 60)
    print("[INFO] OPENING REAL CHROME BROWSER FOR LINKEDIN AUTHENTICATION...")
    print("[INFO] Please log in to your LinkedIn account in the opened window.")
    print("[INFO] Once you reach the LinkedIn Feed, the session will be saved automatically!")
    print("=" * 60)
    
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        context = await browser.new_context(viewport=None)
        page = await context.new_page()
        await page.goto("https://www.linkedin.com/login")
        
        while True:
            await asyncio.sleep(1.5)
            try:
                url = page.url
                if "feed" in url or "mynetwork" in url or "messaging" in url:
                    cookies = await context.cookies()
                    li_at = next((c for c in cookies if c.get("name") == "li_at"), None)
                    if li_at:
                        with open(COOKIE_FILE, "w", encoding="utf-8") as f:
                            json.dump(cookies, f, indent=2)
                        print("\n" + "=" * 60)
                        print("[SUCCESS] 'li_at' SESSION COOKIE CAPTURED AND SAVED!")
                        print("=" * 60)
                        await asyncio.sleep(2)
                        break
            except Exception as e:
                break
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
