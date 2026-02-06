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
export PORT=8099
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
- Start Flask on port `${PORT}` (defaults to `8080` if not set)
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

## Quick Start on a Linux Server (Port 8099)

> Replace `your-public-url.com` with your actual HTTPS domain that points to your server.

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip git

git clone https://your-repo-url.com/Sample_WebApp.git
cd Sample_WebApp

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export TOKEN=your_telegram_bot_token
export URL=https://your-public-url.com
export WEBHOOK_SECRET=your_random_secret
export PORT=8099

python main.py
```

If you need the process to keep running after you close SSH, start it with:

```bash
nohup python main.py > webapp.log 2>&1 &
```

Make sure your firewall allows port `8099`:

```bash
sudo ufw allow 8099
```

## License

GNU GPLv3 - see the LICENSE file for details.
