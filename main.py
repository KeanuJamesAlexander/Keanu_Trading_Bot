import nest_asyncio
import asyncio
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

nest_asyncio.apply()  # Fixes event loop issues on Replit etc.

TOKEN = "8014707054:AAGuYgzHLVsrIB4K2B89F_v1vlio4q5iV08"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome Keanu! Your signal bot is live 🚀")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Example static signal - you can replace this with your AI logic later
    message = (
        "🔥 Trading Signal 🔥\n"
        "Instrument: XAU/USD\n"
        "Action: BUY\n"
        "Entry: 1950\n"
        "Take Profit: 1960\n"
        "Stop Loss: 1945\n"
        "Timeframe: 15m\n"
    )
    await update.message.reply_text(message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/start - Start the bot\n"
        "/signal - Get a trading signal\n"
        "/help - Show this help message"
    )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Set Telegram command list so users can see available commands
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("signal", "Get a trading signal"),
        BotCommand("help", "Show help"),
    ])

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is polling...")
    await app.run_polling()

if __name__ == "__main__":
    # Run the bot, handling event loop issues on Replit/Heroku
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "event loop is running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise