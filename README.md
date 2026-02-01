# Telegram Web App Greeting Bot 👋

A simple Telegram Web App bot that greets users with **"Hi {first_name}"** when they open the WebApp.

## Features

- 👤 **Personalized Greeting** - Shows the user's Telegram first name
- 🔐 **Secure Validation** - HMAC verification of Telegram WebApp data
- 📱 **Responsive UI** - Clean, mobile-friendly layout

## Project Structure

```
.
├── main.py                 # Flask app + Telegram bot handlers
├── validation.py           # Telegram WebApp data validation
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Web app frontend
├── .gitignore
└── README.md
```

## Setup Instructions

### 1) Create a Telegram Bot

1. Open [@BotFather](https://t.me/botfather) in Telegram.
2. Run `/newbot` and follow the prompts to get a **bot token**.

### 2) Host the Web App

You need a public HTTPS URL (Render, Railway, Heroku, or ngrok for local testing).

### 3) Configure Environment Variables

```bash
export TOKEN=your_telegram_bot_token
export URL=https://your-public-url.com
export WEBHOOK_SECRET=your_random_secret
```

### 4) Install Dependencies

```bash
pip install -r requirements.txt
```

### 5) Run the Bot

```bash
python main.py
```

The bot will:
- Start Flask on port `8080`
- Set the Telegram webhook automatically
- Serve the WebApp UI at `/`

### 6) Test in Telegram

1. Open your bot and send `/start`.
2. Tap **"🚀 Open Web App"**.
3. You should see **"Hi {first_name}"** inside the WebApp.

## API Endpoints

- `GET /` - WebApp UI
- `GET /validate` - Validate Telegram WebApp auth
- `POST /webhook/{TOKEN}` - Telegram webhook

## Customization

- Edit `templates/index.html` to change the greeting text or styling.
- Update `main.py` if you want to add more bot commands.

## License

GNU GPLv3 - see the LICENSE file for details.
