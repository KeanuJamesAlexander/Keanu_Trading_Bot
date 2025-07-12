from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import asyncio
import nest_asyncio

# Load token from environment or .env file
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('TOKEN='):
                    TOKEN = line.split('=', 1)[1].strip().strip('"').strip("'")
                    break
    except FileNotFoundError:
        pass

# Validate token
if not TOKEN:
    print("ERROR: No TOKEN found. Please check your .env file or environment variables.")
    exit(1)
else:
    print(f"TOKEN loaded successfully: {TOKEN[:10]}...")  # Only show first 10 chars for security

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome Keanu 👋 Your bot is live!")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 BUY XAU/USD @ 1950\nTP: 1960\nSL: 1945")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - Start\n/signal - Get signal\n/help - Help")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("signal", "Get a signal"),
        BotCommand("help", "Help info")
    ])

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("help", help_command))

    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()  # Apply nest_asyncio to handle existing loop issues
    # Simple approach that works well with Replit
    asyncio.run(main())