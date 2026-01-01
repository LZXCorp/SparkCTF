import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Load the bot token from an environment variable
TOKEN = os.getenv("BOT_TOKEN")

SPECIAL_WORD = "siews assemble NOW"  # Exact case required
BROTHER_LOCATION = "jungsik seoul"

# Dictionary to track users who are in the "waiting for brother location" state
waiting_for_location = {}

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()  # Removed .lower() to preserve case
    
    if text == SPECIAL_WORD:
        await update.message.reply_text(
            "Did you find my brother? Where is he located now? - Hint: the restaurant closest to the picture"
        )
        waiting_for_location[user_id] = True
        return
    
    # Check if user is responding to the brother location question
    if user_id in waiting_for_location and waiting_for_location[user_id]:
        if text.lower() == BROTHER_LOCATION:  # Lowercase only for location check
            await update.message.reply_text("SPARK{th@nks_f0r_f!nding_my_br0}")
            waiting_for_location[user_id] = False
            return
        else:
            # Wrong answer, reset their state
            waiting_for_location[user_id] = False
    
    await update.message.reply_text("I'm not available at the moment.")

def main():
    if not TOKEN:
        raise ValueError("Error: BOT_TOKEN environment variable not set.")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
