import os
import json
import asyncio
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(__file__)
USER_DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "linkedin_user_data"))
COOKIE_FILE = os.path.join(USER_DATA_DIR, "session_cookies.json")

def sanitize_cookies(cookies_list):
    """
    Playwright requires sameSite to be exactly 'Strict', 'Lax', or 'None'.
    Safely handles None values or invalid string types.
    """
    cleaned = []
    for c in cookies_list:
        c_copy = dict(c)
        same_site_raw = c_copy.get("sameSite")
        same_site = str(same_site_raw).lower() if same_site_raw is not None else ""
        
        if same_site in ["no_restriction", "none"]:
            c_copy["sameSite"] = "None"
        elif same_site in ["lax"]:
            c_copy["sameSite"] = "Lax"
        elif same_site in ["strict"]:
            c_copy["sameSite"] = "Strict"
        else:
            c_copy.pop("sameSite", None)
            
        # Clean domain
        domain = c_copy.get("domain", "")
        if not domain:
            c_copy["domain"] = ".linkedin.com"

        cleaned.append(c_copy)
    return cleaned

def is_authenticated():
    if os.path.exists(COOKIE_FILE):
        try:
            with open(COOKIE_FILE, "r", encoding="utf-8") as f:
                cookies = json.load(f)
                return any(c.get("name") == "li_at" and len(c.get("value", "")) > 10 for c in cookies)
        except:
            return False
    return False

def save_cookie_token(li_at_token: str):
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    cookies = [
        {
            "name": "li_at",
            "value": li_at_token.strip(),
            "domain": ".linkedin.com",
            "path": "/",
            "httpOnly": True,
            "secure": True,
            "sameSite": "None"
        }
    ]
    with open(COOKIE_FILE, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2)
    return True

async def launch_interactive_login():
    return {"status": "error", "message": "Please use Method 2 (Cookie JSON paste)."}

async def publish_to_linkedin(text: str, image_paths: list = None):
    if not is_authenticated():
        return {"status": "error", "message": "Not authenticated. Please save your cookies first."}

    try:
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            raw_cookies = json.load(f)
        cookies = sanitize_cookies(raw_cookies)
    except Exception as e:
        return {"status": "error", "message": f"Cookie load error: {str(e)}"}

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, # Visible window so you can watch your post publish!
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            viewport=None,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        await context.add_cookies(cookies)

        page = await context.new_page()
        try:
            await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print(f"[WARN] Feed load warning: {e}")

        await asyncio.sleep(5)

        if "login" in page.url or "checkpoint" in page.url:
            await browser.close()
            return {"status": "error", "message": "LinkedIn redirected to login. Cookies might be expired."}

        try:
            # Click "Start a post" button
            start_btn = page.locator("button:has-text('Start a post')").first
            if await start_btn.is_visible():
                await start_btn.click()
            else:
                await page.locator(".share-box-feed-entry__trigger").click()

            await asyncio.sleep(2)

            # Insert Text into editor
            editor = page.locator("div.ql-editor, div[contenteditable='true']").first
            await editor.click()
            await editor.fill(text)
            await asyncio.sleep(2)

            # Upload Attached Images
            valid_images = [img for img in (image_paths or []) if os.path.exists(img)]
            if valid_images:
                file_input = page.locator("input[type='file']").first
                if await file_input.count() > 0:
                    await file_input.set_input_files(valid_images)
                    await asyncio.sleep(3)
                    next_btn = page.locator("button:has-text('Next')").first
                    if await next_btn.is_visible():
                        await next_btn.click()
                        await asyncio.sleep(2)

            # Click Post / Publish button
            post_btn = page.locator("button.share-actions__primary-action, button:has-text('Post')").first
            if await post_btn.is_visible():
                await post_btn.click()
                await asyncio.sleep(6)
                await browser.close()
                return {"status": "success", "message": f"🎉 SUCCESS! Post published to LinkedIn with {len(valid_images)} image(s)!"}
            else:
                await browser.close()
                return {"status": "partial", "message": "Post draft created in browser. Please click Post to finish."}

        except Exception as e:
            await browser.close()
            return {"status": "error", "message": f"Automation error: {str(e)}"}
