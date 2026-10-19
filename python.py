import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Apni Gemini API key aur Telegram Bot Token yahan dalein
GEMINI_API_KEY = "AQ.Ab8RN6IUzuqhGyYW3UB0Xme02w6UlXgtTvKbXWKOx0m2hNkj3A"
TELEGRAM_BOT_TOKEN = "8921897499:AAEsvTgGthdUvSG5S6LWiBM76C391_0yyRE"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Kuch error aa gaya hai.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
