import nest_asyncio
import asyncio
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import datetime
import random

nest_asyncio.apply()

TOKEN = "8014707054:AAGuYgzHLVsrIB4K2B89F_v1vlio4q5iV08"

# --- Markets and Timeframes ---
MARKETS = ["XAU/USD", "NAS100", "BTC/USD", "EUR/USD", "CRUDE_OIL"]
TIMEFRAMES_ANALYSIS = ["M1", "M5", "M15", "M30", "H1", "H4", "D1"]
TIMEFRAMES_SIGNAL = ["M5", "M15", "M30"]

# --- In-memory historical data placeholder ---
historical_data = {}

# --- Signal storage ---
sent_signals_today = []

# --- Functions for trading logic (stub) ---

def load_historical_data():
    # Placeholder: you would load real data here for AI learning
    for market in MARKETS:
        historical_data[market] = {tf: [] for tf in TIMEFRAMES_ANALYSIS}
    print("Historical data loaded (stub).")

def generate_signal(market, timeframe):
    # Simple random stub for demo
    direction = random.choice(["BUY", "SELL"])
    entry = round(random.uniform(1900, 2000), 2)
    tp = round(entry + random.uniform(5, 15), 2) if direction == "BUY" else round(entry - random.uniform(5, 15), 2)
    sl = round(entry - random.uniform(3, 8), 2) if direction == "BUY" else round(entry + random.uniform(3, 8), 2)
    confidence = round(random.uniform(0.7, 0.99), 2)
    return {
        "market": market,
        "timeframe": timeframe,
        "direction": direction,
        "entry": entry,
        "tp": tp,
        "sl": sl,
        "confidence": confidence
    }

def is_signal_worth(signal):
    # Only send signals with confidence > 0.75 and limit daily signals
    if signal["confidence"] < 0.75:
        return False
    if len(sent_signals_today) >= 12:
        return False
    return True

# --- Telegram command handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome Keanu 👋 Your bot is live! Use /signal to get trading signals.")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Generate and send a signal for a random market and timeframe from allowed signal timeframes
    market = random.choice(MARKETS)
    timeframe = random.choice(TIMEFRAMES_SIGNAL)
    sig = generate_signal(market, timeframe)
    if is_signal_worth(sig):
        msg = (
            f"🚀 {sig['direction']} {sig['market']} @ {sig['entry']}\n"
            f"Timeframe: {sig['timeframe']}\n"
            f"TP: {sig['tp']}\n"
            f"SL: {sig['sl']}\n"
            f"Confidence: {sig['confidence']*100:.0f}%"
        )
        sent_signals_today.append(sig)
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("No good signals available right now. Please try later.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start the bot\n"
        "/signal - Get a trading signal\n"
        "/summary - Get today's summary\n"
        "/help - Show this help"
    )

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not sent_signals_today:
        await update.message.reply_text("No signals have been sent today yet.")
        return

    summary_lines = []
    for sig in sent_signals_today:
        line = (
            f"{sig['direction']} {sig['market']} @ {sig['entry']} (TF: {sig['timeframe']}) "
            f"TP: {sig['tp']} SL: {sig['sl']} Conf: {sig['confidence']*100:.0f}%"
        )
        summary_lines.append(line)
    summary_text = "📊 Today's Signals Summary:\n" + "\n".join(summary_lines)
    await update.message.reply_text(summary_text)

# --- Background task to send daily summary at fixed time ---

async def daily_summary_task(app):
    while True:
        now = datetime.datetime.now()
        # Send summary at 6 PM server time daily
        if now.hour == 18 and now.minute == 0:
            print("Sending daily summary...")
            chat_ids = []  # fill with user chat IDs who subscribed or interact with bot
            # For demo, we skip actual sending to users other than current chat
            # This can be extended with DB or persistent storage to track users

            # You can adapt to broadcast to multiple users if you keep track

            # Reset signals after summary
            sent_signals_today.clear()

        await asyncio.sleep(60)  # check every minute

async def main():
    print("Loading historical data...")
    load_historical_data()

    app = ApplicationBuilder().token(TOKEN).build()

    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("signal", "Get a trading signal"),
        BotCommand("help", "Help info"),
        BotCommand("summary", "Daily signals summary")
    ])

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("summary", summary))

    print("Bot is polling...")
    # Run daily summary task alongside polling
    asyncio.create_task(daily_summary_task(app))
    await app.run_polling()

# Start the bot
asyncio.ensure_future(main())
loop = asyncio.get_event_loop()
loop.run_forever()