import os
import logging
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your tokens
TELEGRAM_BOT_TOKEN = os.getenv("7878301039:AAF0b5EMAQpJoMt2gVLfnriJr3Dk8J0YqVw")
GEMINI_API_KEY = os.getenv("AIzaSyDd4KHxCemlf-uriZVDK9g0ZtqyLdxAmoc")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Flask app for binding to a port
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your Gemini-powered bot. Send me a message, and I'll respond!")

# Message handler for all text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received message: {update.message.text}")
    user_message = update.message.text

    # Get response from Gemini API
    try:
        response = model.generate_content(user_message)
        bot_response = response.text
    except Exception as e:
        logger.error(f"Error generating Gemini response: {e}")
        bot_response = "Sorry, I couldn't generate a response. Please try again."

    # Send response back to Telegram
    await update.message.reply_text(bot_response)

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

# Main function to start the bot
def main():
    logger.info("Starting bot...")
    telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    telegram_app.add_error_handler(error)

    # Start polling (only once)
    logger.info("Polling...")
    telegram_app.run_polling()

# Run Flask and the bot
if __name__ == "__main__":
    import threading

    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080))
    flask_thread.daemon = True
    flask_thread.start()

    # Start the bot
    main()
