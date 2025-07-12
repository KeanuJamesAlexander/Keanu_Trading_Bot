import nest_asyncio
import asyncio
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8014707054:AAGuYgzHLVsrIB4K2B89F_v1vlio4q5iV08"

nest_asyncio.apply()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome Keanu! Bot is online.")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Test Signal: BUY XAU/USD @ 1950\nTP: 1960\nSL: 1945")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commands:\n/start\n/signal\n/help")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("signal", "Get test signal"),
        BotCommand("help", "Show help"),
    ])

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is polling...")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "event loop is running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise