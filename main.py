
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from parser import scrape_top_tweet

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

accounts = [
    "Shashkov_BTC", "vasily_sumanov", "WrappedBTC",
    "Optimism", "SonicLabs", "eulerfinance",
    "unichain", "KrystalDeFi"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Чекаю топ-твиты...")

    for acc in accounts:
        print(f"Чекаю @{acc}...")
        try:
            tweet = await scrape_top_tweet(acc)
            if tweet:
                await update.message.reply_text(tweet[:4096])
            else:
                await update.message.reply_text(f"@{acc}: ничего не найдено")
        except Exception as e:
            print(f"Ошибка @{acc}: {e}")

def main():
    print("Бот запущен")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
