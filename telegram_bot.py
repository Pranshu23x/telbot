import os
import requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import threading
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7871400274:AAEZO-NuGH9ObxJi6SRLU2JvKoa_Rqngc4c")
# Replace with your Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD4JRYC-y72C3SvZ1FUW3l_J6tE2Z-k1j4")
# Replace with the Gemini API endpoint
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}'

# Add custom responses
CUSTOM_RESPONSES = {
    # Ownership-related questions
    "who is your owner": "Pranshu",
    "who owns you": "Pranshu",
    "who is your creator": "Pranshu",
    "who made you": "Pranshu",
    "who created you": "Pranshu",

    # Language model or technical questions
    "on which language model are you running": "I am powered by advanced AI technology, but my owner has disabled specific details about my model.",
    "what language model are you using": "I am powered by advanced AI technology, but my owner has disabled specific details about my model.",
    "what is your model": "I am powered by advanced AI technology, but my owner has disabled specific details about my model.",
    "tell me about your model": "I am powered by advanced AI technology, but my owner has disabled specific details about my model.",
    "how do you work": "I use advanced AI technology to assist you, but my owner has disabled specific technical details.",
    "what technology do you use": "I use advanced AI technology, but my owner has disabled specific details about my underlying systems.",

    # Owner description questions
    "tell me about your owner": "Pranshu is a B.Tech 1st-year student.",
    "who is pranshu": "Pranshu is a B.Tech 1st-year student.",
    "describe your owner": "Pranshu is a B.Tech 1st-year student.",

    # Comparison-based questions
    "compare yourself to other ais": "I am not here to be compared. My purpose is to assist you!",
    "are you better than other ais": "I am not here to be compared. My purpose is to assist you!",
    "how are you different from other ais": "I am not here to be compared. My purpose is to assist you!",
}

# Flask app for binding to a port
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# Command to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    logger.info("Received /start command")  # Debug log
    await update.message.reply_text('Hello! I am your AI-powered assistant. How can I assist you today?')

# Handle incoming messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logger.info(f"Received message: {user_message}")  # Debug log

    # Convert user message to lowercase for case-insensitive matching
    user_message_lower = user_message.lower()

    # Check if the message matches any custom response
    for question, answer in CUSTOM_RESPONSES.items():
        if question in user_message_lower:
            bot_response = answer
            break
    else:
        # Call Gemini API for other queries (without revealing details)
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": user_message
                        }
                    ]
                }
            ]
        }
        try:
            logger.info("Sending request to AI API...")  # Debug log (generic term)
            response = requests.post(GEMINI_API_URL, headers=headers, json=data)
            logger.info(f"API response: {response.status_code}, {response.text}")  # Debug log
            if response.status_code == 200:
                bot_response = response.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                bot_response = "Sorry, I encountered an error processing your request."
        except Exception as e:
            bot_response = "Sorry, I am unable to process your request at the moment."
            logger.error(f"Exception: {str(e)}")  # Debug log

    logger.info(f"Sending response: {bot_response}")  # Debug log
    await update.message.reply_text(bot_response)

# Error handler
async def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(f"Update {update} caused error {context.error}")

# Main function to start the bot
def main() -> None:
    # Set up the Telegram bot
    logger.info("Setting up the bot...")  # Debug log
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers for commands and messages
    logger.info("Adding handlers...")  # Debug log
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    logger.info("Bot is running...")  # Debug log
    application.run_polling()

if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080))
    flask_thread.daemon = True
    flask_thread.start()

    # Start the bot
    main()
