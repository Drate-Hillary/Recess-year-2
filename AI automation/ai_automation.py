from datetime import datetime
from dotenv import load_dotenv
import os
from telegram import Bot, Update
import asyncio
from transformers import pipeline
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import torch
import sys
import logging

# Set up basic logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Initialize AI agent
def initialize_ai_model():
    try:
        model_name = "distilgpt2"
        device = 0 if torch.cuda.is_available() else -1
        print(f"Device set to use {'cuda' if device == 0 else 'cpu'}")
        generator = pipeline("text-generation", model=model_name, device=device)
        print(f"Initialized AI model: {model_name}")
        return generator
    except Exception as e:
        print(f'Failed to initialize AI model: {e}')
        return None

generator = initialize_ai_model()

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if generator is None:
            await update.message.reply_text("AI model is not available")
            return
            
        user_msg = update.message.text
        ai_response = generator(user_msg, max_new_tokens=50)[0]["generated_text"]
        await update.message.reply_text(ai_response)
    except Exception as e:
        await update.message.reply_text(f"Sorry, an error occurred: {e}")

async def main():
    app = None
    try:
        # Create application
        app = ApplicationBuilder().token(telegram_bot_token).build()
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("Bot is running...")
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        
        # Run until Ctrl+C
        while True:
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"Bot failed to start: {e}")
    finally:
        if app is not None:
            print("Shutting down bot...")
            try:
                if app.updater:
                    await app.updater.stop()
                await app.stop()
                await app.shutdown()
            except Exception as e:
                print(f"Error during shutdown: {e}")

if __name__ == "__main__":
    if sys.platform.startswith('win') and sys.version_info >= (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"Unexpected error: {e}")