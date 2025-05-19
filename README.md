# 💱 Currency Converter Telegram Bot

This is a Telegram bot that converts currencies using natural language. Just send a message like:

- `Convert 100 USD to INR`  
- `How much is 50 euros in rupees?`  
- `25 yen in usd`

The bot intelligently parses your message using regular expressions and GPT, then fetches real-time exchange rates using the [ExchangeRate API](https://www.exchangerate-api.com/).

---

## ✨ Features

- 💬 Understands natural language queries  
- 🔍 Uses regex and OpenAI's GPT to extract conversion details  
- 🌍 Fetches live currency rates from ExchangeRate API  
- 🤖 Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)  
- 🚀 Deployable on [Render](https://render.com) with minimal setup

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/currency-bot.git
cd currency-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file or export them in your terminal:

```bash
export TELEGRAM_BOT_TOKEN=your_token
export OPENAI_API_KEY=your_openai_key
export EXCHANGE_API_KEY=your_exchange_key
```

### 4. Run the bot

```bash
python bot.py
```

---

## 🧠 Powered By

- OpenAI GPT (for parsing natural language)  
- ExchangeRate API (for live exchange rates)  
- python-telegram-bot (Telegram integration)

---

## 📦 Deploy to Render

This project includes a `render.yaml` file for one-click deployment to [Render](https://render.com/).
