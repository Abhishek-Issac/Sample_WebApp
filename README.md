# Word Magic Telegram Web App Bot ✨

A beautiful and interactive Telegram Web App bot built with Python that generates random words and inspirational sentences from a customizable word list.

## Features

- 🎨 **Modern UI Design** - Gradient backgrounds, smooth animations, and glass-morphism effects
- 👤 **User Authentication** - Secure validation of Telegram WebApp data
- 🎲 **Random Word Generator** - Pick random words from a curated list
- 💬 **Magic Sentences** - Generate personalized inspirational messages
- 📱 **Responsive Design** - Works seamlessly on all devices
- ✨ **Haptic Feedback** - Interactive vibrations for better UX (on supported devices)

## Project Structure

```
.
├── main.py                 # Main Flask application with bot handlers
├── validation.py           # Telegram WebApp data validation
├── words.txt              # Word list for random generation
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Web app frontend with beautiful UI
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (get one from [@BotFather](https://t.me/botfather))
- A publicly accessible URL for hosting (e.g., Render, Railway, Heroku, or ngrok for local testing)

### Environment Variables

Set the following environment variables:

```bash
TOKEN=your_telegram_bot_token
URL=https://your-app-url.com
WEBHOOK_SECRET=your_secure_random_string
```

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Customize the word list:**
Edit `words.txt` to add your own words (one word per line)

4. **Run the application:**
```bash
python main.py
```

The bot will automatically:
- Initialize the Telegram bot
- Set up webhooks
- Start the Flask web server on port 8080

## How to Use

1. **Start the bot** - Send `/start` to your bot on Telegram
2. **Open Web App** - Click the "🚀 Open Web App" button
3. **Explore features:**
   - View your Telegram user information
   - Generate random words from the word list
   - Create personalized inspirational sentences
   - Enjoy the smooth animations and beautiful UI

## API Endpoints

- `GET /` - Main web app page
- `GET /validate` - Validate Telegram WebApp authentication
- `GET /random-word` - Get a random word from the word list
- `GET /random-sentence` - Generate a random personalized sentence
- `POST /bots/{TOKEN}` - Webhook endpoint for Telegram updates

## Customization

### Adding More Words

Edit `words.txt` and add one word per line:
```
amazing
wonderful
fantastic
...
```

### Modifying Sentence Templates

In `main.py`, edit the `templates` list in the `/random-sentence` endpoint:
```python
templates = [
    f"You are truly {random.choice(WORD_LIST)}, {user_data['first_name']}!",
    # Add your own templates here
]
```

### Styling the UI

Edit `templates/index.html` to customize:
- Colors and gradients
- Animations
- Layout
- Font styles

## Security Features

- ✅ HMAC-SHA256 validation of WebApp data
- ✅ Webhook secret token verification
- ✅ Secure authentication for all API endpoints
- ✅ No sensitive data exposure

## Technologies Used

- **Backend:** Python, Flask, python-telegram-bot
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** Telegram WebApp API with HMAC validation
- **Styling:** Modern CSS with gradients, animations, and glassmorphism

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Acknowledgments

- Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Inspired by modern web design trends
- Telegram WebApp API documentation

---

Made with ❤️ for the Telegram community
