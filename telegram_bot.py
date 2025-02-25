import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your tokens
TELEGRAM_BOT_TOKEN = "7878301039:AAF0b5EMAQpJoMt2gVLfnriJr3Dk8J0YqVw"
GEMINI_API_KEY = "AIzaSyA0MUWVJyg4K13q3JGPgKzUzUoN8_hd_vU"

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your Gemini-powered bot. Send me a message, and I'll respond!")

# Message handler for all text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Get response from Gemini API
    response = model.generate_content(user_message)
    bot_response = response.text

    # Send response back to Telegram
    await update.message.reply_text(bot_response)

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Main function to start the bot
def main():
    print("Starting bot...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    # Start polling
    print("Polling...")
    app.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()
