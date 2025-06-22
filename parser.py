from playwright.async_api import async_playwright, TimeoutError

async def scrape_top_tweet(username):
    url = f"https://twitter.com/{username}"
    top = None

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            xhrs = []

            page.on("response", lambda resp: xhrs.append(resp) if "TweetResultByRestId" in resp.url else None)
            await page.goto(url, timeout=20000)
            await page.wait_for_timeout(5000)

            for r in xhrs:
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

    except TimeoutError:
        return f"❌ Не удалось загрузить твиттер {username} — таймаут"
    except Exception as e:
        return f"❌ Ошибка: {e}"

    if not top:
        return f"ℹ️ У @{username} нет популярных твитов, но, возможно, он просто неактивен."

    return f"@{username}\n❤️ {top['likes']} лайков\n📅 {top['date']}\n🔗 https://twitter.com/{username}/status/{top['id']}\n📝 {top['content']}"
