from playwright.async_api import async_playwright

async def scrape_top_tweet(username):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(f"https://x.com/{username}")
            await page.wait_for_selector("article", timeout=10000)
            tweet = await page.locator("article").first.inner_text()
            await browser.close()
            return tweet.split("\n")[0]
    except Exception as e:
        return None
