import logging
import os
import asyncio
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

import config
import database
from handlers import (
    start_command,
    help_command,
    husband_command,
    wife_command,
    son_command,
    daughter_command,
    couple_command,
    track_users,
    post_init
)

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# --- FLASK APP SETUP (For Render Port Binding) ---
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Random Relationship Bot is running! 🤖❤️"

def run_flask():
    """Function to run Flask server on the port provided by Render."""
    port = int(os.environ.get('PORT', 5000))
    app_flask.run(host='0.0.0.0', port=port)

# --- TELEGRAM BOT SETUP ---
async def setup_bot():
    """Async function to initialize and run the Telegram Bot."""
    if not config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing! Please set it in your environment variables.")

    # Initialize SQLite Database
    database.init_db()

    # Build the application
    app = ApplicationBuilder().token(config.BOT_TOKEN).post_init(post_init).build()

    # Register Command Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("husband", husband_command))
    app.add_handler(CommandHandler("wife", wife_command))
    app.add_handler(CommandHandler("son", son_command))
    app.add_handler(CommandHandler("daughter", daughter_command))
    app.add_handler(CommandHandler("couple", couple_command))

    # Register Message Handler to track all users
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, track_users))

    logger.info("Starting Random Relationship Bot Polling...")
    
    # Start Polling
    await app.initialize()
    await app.updater.start_polling(drop_pending_updates=True)
    await app.start()

    # Keep the async loop running forever
    while True:
        await asyncio.sleep(3600)

def run_bot():
    """Wrapper to create a new event loop for the background thread (Fixes Python 3.10+ issues)."""
    # Create a new event loop for this specific thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Run the async setup_bot function inside this loop
        loop.run_until_complete(setup_bot())
    except Exception as e:
        logger.error(f"Bot thread crashed: {e}")
    finally:
        loop.close()

def main() -> None:
    # Start Telegram bot in a separate background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("Telegram Bot thread started in background.")

    # Run Flask in the main thread to bind the PORT for Render
    logger.info("Starting Flask server for Render port binding...")
    run_flask()

if __name__ == "__main__":
    main()
