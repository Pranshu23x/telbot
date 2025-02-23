import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Replace with your Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7420321518:AAHS0xJL3HXfBd-G3EkbWbG9rznAQPJfBfs'
# Replace with your Gemini API key
GEMINI_API_KEY = 'AIzaSyA0MUWVJyg4K13q3JGPgKzUzUoN8_hd_vU'
# Replace with the Gemini API endpoint
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}'

# Command to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    print("Received /start command")  # Debug log
    await update.message.reply_text('Hi, ask me anything')

# Handle incoming messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    print(f"Received message: {user_message}")  # Debug log

    # Call Gemini API
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
        print("Sending request to Gemini API...")  # Debug log
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        print(f"API response: {response.status_code}, {response.text}")  # Debug log
        if response.status_code == 200:
            bot_response = response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            bot_response = f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        bot_response = f"An error occurred: {str(e)}"
        print(f"Exception: {str(e)}")  # Debug log

    print(f"Sending response: {bot_response}")  # Debug log
    await update.message.reply_text(bot_response)

# Main function to start the bot
def main() -> None:
    # Set up the Telegram bot
    print("Setting up the bot...")  # Debug log
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers for commands and messages
    print("Adding handlers...")  # Debug log
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running...")  # Debug log
    application.run_polling()

if __name__ == '__main__':
    main()