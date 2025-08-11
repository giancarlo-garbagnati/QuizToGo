import asyncio
from playwright.async_api import async_playwright
from config import Config

async def login_and_save_state(cfg: Config):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=cfg.headless)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(cfg.base_url, wait_until="networkidle")

        # TODO: Replace selectors with actual login form fields/buttons
        await page.click("text=Log In")
        await page.fill("input[name='email']", cfg.username)
        await page.fill("input[name='password']", cfg.password)
        await page.click("button[type='submit']")

        # Optional: pause to handle 2FA manually during first run
        # await page.pause()

        # Wait for a known post-login element to ensure success
        await page.wait_for_selector("nav >> text=My Account")

        # Save session state
        await context.storage_state(path=cfg.storage_state)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(login_and_save_state(Config()))
