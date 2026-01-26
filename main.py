import os
import logging
import random
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

# Load word list
def load_words():
    """Load words from words.txt file."""
    try:
        with open('words.txt', 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["amazing", "wonderful", "fantastic", "incredible", "awesome"]

WORD_LIST = load_words()

# Create Flask app
app = Flask(__name__)

# Create bot application
bot_app = Application.builder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    bot_username = (await context.bot.get_me()).username
    
    keyboard = [[
        InlineKeyboardButton(
            "🚀 Open Web App",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Hello, I'm @{bot_username}!\n\n"
        f"Welcome to the Word Magic Web App! ✨\n"
        f"Click the button below to experience something special!",
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
        return jsonify({"error": "Missing authentication"}), 400
    
    # Validate the data
    try:
        user_data = validate_webapp_data(init_data, TOKEN)
        return jsonify({
            "success": True,
            "user": user_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 401


@app.route('/random-word')
def random_word():
    """Get a random word from the word list."""
    init_data = request.headers.get('X-Auth')
    if not init_data:
        return jsonify({"error": "Missing authentication"}), 400
    
    try:
        from validation import validate_webapp_data
        validate_webapp_data(init_data, TOKEN)
        
        word = random.choice(WORD_LIST)
        return jsonify({"word": word})
    except Exception as e:
        return jsonify({"error": str(e)}), 401


@app.route('/random-sentence')
def random_sentence():
    """Generate a random sentence using words from the word list."""
    init_data = request.headers.get('X-Auth')
    if not init_data:
        return jsonify({"error": "Missing authentication"}), 400
    
    try:
        from validation import validate_webapp_data
        user_data = validate_webapp_data(init_data, TOKEN)
        
        # Generate random sentence
        templates = [
            f"You are truly {random.choice(WORD_LIST)}, {user_data['first_name']}!",
            f"Today feels {random.choice(WORD_LIST)} and {random.choice(WORD_LIST)}!",
            f"Your {random.choice(WORD_LIST)} spirit makes the world {random.choice(WORD_LIST)}!",
            f"Stay {random.choice(WORD_LIST)}, stay {random.choice(WORD_LIST)}!",
            f"{user_data['first_name']}, you're absolutely {random.choice(WORD_LIST)}!",
        ]
        
        sentence = random.choice(templates)
        return jsonify({"sentence": sentence})
    except Exception as e:
        return jsonify({"error": str(e)}), 401


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
