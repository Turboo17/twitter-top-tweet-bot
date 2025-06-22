from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from parser import scrape_top_tweet
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tweet = await scrape_top_tweet("vasily_sumanov")
    if tweet:
        await update.message.reply_text(tweet)
    else:
        await update.message.reply_text("Твит не найден 😔")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    import asyncio
    async def main():
        await app.initialize()
        await app.start()
        await app.bot.set_webhook(WEBHOOK_URL)
        await app.updater.start_webhook(
            listen="0.0.0.0",
            port=8000,
            webhook_url=WEBHOOK_URL,
        )
        await app.updater.idle()

    asyncio.run(main())
