import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Environment variable se token lega (SAFE)
TOKEN = os.environ.get('TOKEN')
YOUR_USER_ID = 7213637077

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f'Namaste {user.first_name}! Main aapka message owner tak pahuncha dunga.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Koi bhi message bhejiye, main owner ko forward kar dunga.')

def forward_to_owner(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        message_text = update.message.text
        
        context.bot.send_message(
            chat_id=YOUR_USER_ID, 
            text=f"📩 New message from {user_name} (ID: {user_id}):\n\n{message_text}"
        )
        
        update.message.reply_text("✅ Aapka message bhej diya gaya hai!")
    except Exception as e:
        logger.error(f"Error in forwarding: {e}")

def handle_owner_reply(update: Update, context: CallbackContext) -> None:
    try:
        if update.message.from_user.id == YOUR_USER_ID and update.message.reply_to_message:
            replied_msg = update.message.reply_to_message.text
            
            if "New message from" in replied_msg and "(ID:" in replied_msg:
                start_idx = replied_msg.find("(ID:") + 4
                end_idx = replied_msg.find(")", start_idx)
                user_id = int(replied_msg[start_idx:end_idx])
                
                context.bot.send_message(
                    chat_id=user_id, 
                    text=f"📨 Owner ka reply: {update.message.text}"
                )
                update.message.reply_text("✅ Reply bhej diya gaya!")
    except Exception as e:
        logger.error(f"Error in replying: {e}")
        update.message.reply_text(f"❌ Error: {str(e)}")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command & ~Filters.reply, forward_to_owner))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.reply, handle_owner_reply))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
