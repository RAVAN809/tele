import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Safe way - environment variable se lega
TOKEN = os.environ.get('TOKEN')
YOUR_USER_ID = 7213637077  # Aapka user ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f'🚀 Namaste {user.first_name}!\n\nMera naam Ravan Bot hai aur main aapke messages owner tak pahunchata hoon.')

def help_cmd(update: Update, context: CallbackContext) -> None:
    help_text = """
🤖 **Bot Commands:**
/start - Bot ko start karein
/help - Help message dikhayein
/status - Bot status check karein

📩 **Simply koi bhi message bhej dena, main owner tak pahuncha dunga.**
"""
    update.message.reply_text(help_text, parse_mode='Markdown')

def status(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('✅ Bot perfectly kaam kar raha hai!')

def forward_to_owner(update: Update, context: CallbackContext) -> None:
    try:
        user = update.effective_user
        chat = update.effective_chat
        
        # User information
        user_info = f"👤 Name: {user.first_name}"
        if user.last_name:
            user_info += f" {user.last_name}"
        user_info += f"\n🆔 ID: {user.id}"
        user_info += f"\n📛 Username: @{user.username}" if user.username else "\n📛 Username: Not available"
        
        # Message information
        message_info = f"\n💬 Message: {update.message.text}"
        
        # Forward to owner
        context.bot.send_message(
            chat_id=YOUR_USER_ID,
            text=f"📨 **New Message Received**\n\n{user_info}{message_info}",
            parse_mode='Markdown'
        )
        
        # Confirm to user
        update.message.reply_text('✅ Your message has been forwarded to the owner!')
        
    except Exception as e:
        logger.error(f"Forward error: {e}")
        update.message.reply_text('❌ Error forwarding message.')

def handle_owner_reply(update: Update, context: CallbackContext) -> None:
    try:
        # Check if message is from owner and is a reply
        if update.message.from_user.id == YOUR_USER_ID and update.message.reply_to_message:
            replied_msg = update.message.reply_to_message.text
            
            # Extract user ID from replied message
            if "🆔 ID:" in replied_msg:
                lines = replied_msg.split('\n')
                user_id = None
                for line in lines:
                    if "🆔 ID:" in line:
                        user_id = int(line.split(":")[1].strip())
                        break
                
                if user_id:
                    # Send message to user
                    context.bot.send_message(
                        chat_id=user_id,
                        text=f"📩 **Reply from Owner:**\n\n{update.message.text}"
                    )
                    update.message.reply_text('✅ Reply sent successfully!')
                else:
                    update.message.reply_text('❌ User ID not found in message.')
                    
    except Exception as e:
        logger.error(f"Reply error: {e}")
        update.message.reply_text(f'❌ Error: {str(e)}')

def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    try:
        updater = Updater(TOKEN)
        dispatcher = updater.dispatcher

        # Add handlers
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_cmd))
        dispatcher.add_handler(CommandHandler("status", status))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_to_owner))
        dispatcher.add_handler(MessageHandler(Filters.text & Filters.reply, handle_owner_reply))
        dispatcher.add_error_handler(error_handler)

        # Start the bot
        logger.info("Bot starting...")
        updater.start_polling()
        logger.info("Bot started successfully!")
        updater.idle()
        
    except Exception as e:
        logger.error(f"Bot failed to start: {e}")

if __name__ == '__main__':
    main()
