
from playwright.async_api import async_playwright

async def scrape_top_tweet(username):
    url = f"https://twitter.com/{username}"
    top = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        xhrs = []

        page.on("response", lambda resp: xhrs.append(resp) if resp.request.resource_type == "xhr" else None)
        await page.goto(url)
        await page.wait_for_timeout(5000)

        for r in xhrs:
            if "TweetResultByRestId" in r.url:
                try:
                    data = await r.json()
                    result = data.get('data', {}).get('tweetResult', {}).get('result')
                    if result:
                        legacy = result.get('legacy', {})
                        if not top or legacy.get("favorite_count", 0) > top["likes"]:
                            top = {
                                "likes": legacy.get("favorite_count", 0),
                                "date": legacy.get("created_at"),
                                "content": legacy.get("full_text"),
                                "id": legacy.get("id_str")
                            }
                except:
                    continue

        await browser.close()

    if not top:
        return None

    return f"@{username}\n❤️ {top['likes']} лайков\n📅 {top['date']}\n🔗 https://twitter.com/{username}/status/{top['id']}\n📝 {top['content']}"
