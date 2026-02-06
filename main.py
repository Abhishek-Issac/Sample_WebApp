#!/usr/bin/env python3
"""
Telegram Web App Bot - Word Magic
A beautiful web app bot with random word and sentence generation.
"""

import os
import logging
import random
from flask import Flask, render_template, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Suppress httpx logs
logging.getLogger("httpx").setLevel(logging.WARNING)

# Get environment variables
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ TOKEN environment variable is required")

WEBAPP_URL = os.getenv("URL")
if not WEBAPP_URL:
    raise ValueError("❌ URL environment variable is required")

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "default_secret_change_me")
PORT = int(os.getenv("PORT", "8080"))

# Load word list
def load_words():
    """Load words from words.txt file."""
    try:
        with open('words.txt', 'r') as f:
            words = [line.strip() for line in f if line.strip()]
            logger.info(f"✅ Loaded {len(words)} words from words.txt")
            return words
    except FileNotFoundError:
        logger.warning("⚠️ words.txt not found, using default words")
        return ["amazing", "wonderful", "fantastic", "incredible", "awesome", 
                "brilliant", "creative", "delightful", "energetic", "graceful"]

WORD_LIST = load_words()

# Create Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Global bot application
bot_app = None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    try:
        user = update.effective_user
        bot_info = await context.bot.get_me()
        
        keyboard = [[
            InlineKeyboardButton(
                "🚀 Open Web App",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = (
            f"👋 Hello {user.first_name}!\n\n"
            f"I'm @{bot_info.username}, your Word Magic companion! ✨\n\n"
            f"Click the button below to explore random words and "
            f"generate inspiring sentences!\n\n"
            f"Let the magic begin! 🎯"
        )
        
        await update.message.reply_text(message, reply_markup=reply_markup)
        logger.info(f"✅ /start command sent to {user.first_name} (ID: {user.id})")
        
    except Exception as e:
        logger.error(f"❌ Error in start command: {e}", exc_info=True)


# Flask Routes

@app.route('/')
def index():
    """Serve the main web app page."""
    logger.info("📱 Web app accessed")
    return render_template('index.html', webapp_url=WEBAPP_URL)


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "bot": "running"}), 200


@app.route('/validate')
def validate():
    """Validate Telegram WebApp data."""
    from validation import validate_webapp_data
    
    init_data = request.headers.get('X-Auth')
    if not init_data:
        logger.warning("❌ Validation failed: Missing X-Auth header")
        return jsonify({"error": "Missing authentication"}), 400
    
    try:
        user_data = validate_webapp_data(init_data, TOKEN)
        logger.info(f"✅ User authenticated: {user_data.get('first_name')} (ID: {user_data.get('id')})")
        return jsonify({
            "success": True,
            "user": user_data
        })
    except Exception as e:
        logger.error(f"❌ Validation error: {e}")
        return jsonify({"error": str(e)}), 401


@app.route('/random-word')
def get_random_word():
    """Get a random word from the word list."""
    from validation import validate_webapp_data
    
    init_data = request.headers.get('X-Auth')
    if not init_data:
        return jsonify({"error": "Missing authentication"}), 400
    
    try:
        validate_webapp_data(init_data, TOKEN)
        word = random.choice(WORD_LIST)
        logger.info(f"🎲 Random word generated: {word}")
        return jsonify({"word": word})
    except Exception as e:
        logger.error(f"❌ Random word error: {e}")
        return jsonify({"error": str(e)}), 401


@app.route('/random-sentence')
def get_random_sentence():
    """Generate a random sentence using words from the word list."""
    from validation import validate_webapp_data
    
    init_data = request.headers.get('X-Auth')
    if not init_data:
        return jsonify({"error": "Missing authentication"}), 400
    
    try:
        user_data = validate_webapp_data(init_data, TOKEN)
        first_name = user_data.get('first_name', 'friend')
        
        # Sentence templates
        templates = [
            f"You are truly {random.choice(WORD_LIST)}, {first_name}! 🌟",
            f"Today feels {random.choice(WORD_LIST)} and {random.choice(WORD_LIST)}! ✨",
            f"Your {random.choice(WORD_LIST)} spirit makes the world {random.choice(WORD_LIST)}! 🌈",
            f"Stay {random.choice(WORD_LIST)}, stay {random.choice(WORD_LIST)}! 💪",
            f"{first_name}, you're absolutely {random.choice(WORD_LIST)}! 🎯",
            f"Keep being {random.choice(WORD_LIST)}, {first_name}! You inspire others! 🚀",
            f"Your {random.choice(WORD_LIST)} energy is {random.choice(WORD_LIST)}! ⚡",
        ]
        
        sentence = random.choice(templates)
        logger.info(f"💬 Sentence generated for {first_name}")
        return jsonify({"sentence": sentence})
    except Exception as e:
        logger.error(f"❌ Random sentence error: {e}")
        return jsonify({"error": str(e)}), 401


@app.route(f'/webhook/{TOKEN}', methods=['POST'])
def webhook_handler():
    """Handle incoming webhook updates from Telegram."""
    secret_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    
    if secret_token != WEBHOOK_SECRET:
        logger.warning("❌ Unauthorized webhook attempt")
        return "Unauthorized", 401
    
    try:
        import asyncio
        update_data = request.get_json(force=True)
        update = Update.de_json(update_data, bot_app.bot)
        
        # Process update synchronously in the context of the running event loop
        asyncio.run(bot_app.process_update(update))
        
        return "OK", 200
    except Exception as e:
        logger.error(f"❌ Webhook processing error: {e}", exc_info=True)
        return "Error", 500


def setup_bot():
    """Initialize the Telegram bot."""
    global bot_app
    
    import asyncio
    
    logger.info("🤖 Initializing Telegram bot...")
    
    # Create application
    bot_app = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    bot_app.add_handler(CommandHandler("start", start_command))
    
    # Initialize and setup webhook
    async def init_bot():
        await bot_app.initialize()
        await bot_app.start()
        
        # Set webhook
        webhook_url = f"{WEBAPP_URL}/webhook/{TOKEN}"
        await bot_app.bot.set_webhook(
            url=webhook_url,
            max_connections=100,
            drop_pending_updates=True,
            secret_token=WEBHOOK_SECRET,
            allowed_updates=["message", "callback_query"]
        )
        
        # Get bot info
        bot_info = await bot_app.bot.get_me()
        
        logger.info("=" * 60)
        logger.info(f"✅ Bot successfully started!")
        logger.info(f"🤖 Bot Username: @{bot_info.username}")
        logger.info(f"🆔 Bot ID: {bot_info.id}")
        logger.info(f"📡 Webhook URL: {webhook_url}")
        logger.info(f"🌐 Web App URL: {WEBAPP_URL}")
        logger.info(f"📚 Words loaded: {len(WORD_LIST)}")
        logger.info("=" * 60)
    
    # Run initialization
    asyncio.run(init_bot())
    logger.info("✅ Bot initialization complete")


def main():
    """Main entry point."""
    try:
        logger.info("🚀 Starting Word Magic Bot...")
        logger.info(f"📍 Web App URL: {WEBAPP_URL}")
        
        # Setup bot
        setup_bot()
        
        # Start Flask server
        logger.info(f"🌐 Starting Flask web server on port {PORT}...")
        app.run(
            host='0.0.0.0',
            port=8099,
            debug=False,
            use_reloader=False
        )
        
    except KeyboardInterrupt:
        logger.info("⏹️ Shutting down gracefully...")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()
