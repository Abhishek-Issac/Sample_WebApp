import os
import logging
from flask import Flask, render_template, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get environment variables
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable is empty")

WEBAPP_URL = os.getenv("URL")
if not WEBAPP_URL:
    raise ValueError("URL environment variable is empty")

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
if not WEBHOOK_SECRET:
    raise ValueError("WEBHOOK_SECRET environment variable is empty")

# Create Flask app
app = Flask(__name__)

# Create bot application
bot_app = Application.builder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    bot_username = (await context.bot.get_me()).username
    
    keyboard = [[
        InlineKeyboardButton(
            "Press me",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Hello, I'm @{bot_username}.\n"
        f"You can use me to run a (very) simple telegram webapp demo!",
        reply_markup=reply_markup
    )


@app.route('/')
def index():
    """Serve the index page."""
    return render_template('index.html', webapp_url=WEBAPP_URL)


@app.route('/validate')
def validate():
    """Validate the webapp data."""
    from validation import validate_webapp_data
    
    # Get the initData from X-Auth header
    init_data = request.headers.get('X-Auth')
    if not init_data:
        return "validation failed; missing X-Auth header", 400
    
    # Validate the data
    try:
        user_data = validate_webapp_data(init_data, TOKEN)
        return f"validation success; user '{user_data['first_name']}' is authenticated (id: {user_data['id']})."
    except Exception as e:
        return f"validation failed; error: {str(e)}", 401


@app.route(f'/bots/{TOKEN}', methods=['POST'])
async def webhook():
    """Handle incoming webhook updates from Telegram."""
    # Verify secret token
    secret_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    if secret_token != WEBHOOK_SECRET:
        return "Unauthorized", 401
    
    # Process update
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    
    return "OK"


async def setup_webhook():
    """Set up the webhook."""
    webhook_url = f"{WEBAPP_URL}/bots/{TOKEN}"
    await bot_app.bot.set_webhook(
        url=webhook_url,
        max_connections=100,
        drop_pending_updates=True,
        secret_token=WEBHOOK_SECRET
    )
    logger.info(f"Webhook set to: {webhook_url}")


def main():
    """Start the bot."""
    # Add handlers
    bot_app.add_handler(CommandHandler("start", start))
    
    # Initialize the bot application
    asyncio.run(bot_app.initialize())
    asyncio.run(bot_app.start())
    
    # Set up webhook
    asyncio.run(setup_webhook())
    
    bot_username = asyncio.run(bot_app.bot.get_me()).username
    logger.info(f"Bot has been started... bot_username: {bot_username}")
    
    # Start Flask server
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
