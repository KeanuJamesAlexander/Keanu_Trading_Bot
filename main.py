import os
import nest_asyncio
import asyncio
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

nest_asyncio.apply()  # Patch event loop for environments like Replit

TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    print("ERROR: TOKEN not found in environment variables!")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome Keanu 👋 Your bot is live!")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 BUY XAU/USD @ 1950\nTP: 1960\nSL: 1945")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - Start\n/signal - Get signal\n/help - Help")

async def main():
    print("Starting bot...")
    app = ApplicationBuilder().token(TOKEN).build()

    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("signal", "Get a signal"),
        BotCommand("help", "Help info")
    ])

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is polling...")
    await app.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except RuntimeError as e:
        print(f"Caught runtime error: {e}")
        # If event loop already running, run in existing loop
        asyncio.ensure_future(main())
        loop.run_forever()