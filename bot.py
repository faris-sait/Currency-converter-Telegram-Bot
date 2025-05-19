from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import openai
import re
import os
# Set your keys
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💱 Hi! Just type a message like:\n- Convert 100 USD to INR\n- How much is 50 euros in rupees?\n- 25 yen in usd"
    )

def get_conversion(amount, from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{from_currency.upper()}"
    response = requests.get(url)
    data = response.json()

    if data["result"] != "success":
        return "⚠️ Could not fetch exchange rates. Check your currency codes."

    rate = data["conversion_rates"].get(to_currency.upper())
    if not rate:
        return "❌ Invalid target currency."

    converted = round(float(amount) * rate, 2)
    return f"{amount} {from_currency.upper()} = {converted} {to_currency.upper()}"

def parse_with_regex(text):
    pattern = r"(\d+(?:\.\d+)?)\s*([A-Za-z]{3})\s*(?:to|in)\s*([A-Za-z]{3})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return float(match.group(1)), match.group(2).upper(), match.group(3).upper()
    return None

def parse_with_gpt(message: str):
    prompt = f"""
Extract currency conversion info from this message:
"{message}"

Respond with a JSON like:
{{"amount": 100, "from": "USD", "to": "INR"}}

If you can't extract, say "None".
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    reply = response.choices[0].message.content.strip()
    try:
        import json
        return json.loads(reply)
    except:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Try regex first
    parsed = parse_with_regex(text)
    if parsed:
        amount, from_curr, to_curr = parsed
        result = get_conversion(amount, from_curr, to_curr)
        await update.message.reply_text(result)
        return

    # Fallback to GPT
    gpt_result = parse_with_gpt(text)
    if gpt_result and "amount" in gpt_result:
        amount = gpt_result["amount"]
        from_curr = gpt_result["from"]
        to_curr = gpt_result["to"]
        result = get_conversion(amount, from_curr, to_curr)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("❗ Sorry, I couldn’t understand that. Try: '100 USD to INR'")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot is running...")
    app.run_polling()

