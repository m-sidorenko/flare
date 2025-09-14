from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.utils import get_logger

logger = get_logger()

greeting_text_md = """
Hi *{user_name}* 👋
Welcome to *Flare*

I am here to help you receive alerts from Logfire directly in your Telegram chats, groups, and channels.
Let's get started! 🎇
"""

async def _start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command.
    Sends a welcome message
    """
    logger.info(f"Received '/start' command from user: {update.effective_user.name}")
    try:
        # send msg
        await update.message.reply_text(
            text=greeting_text_md.format(
                user_name=update.effective_user.first_name
            ),
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error handling '/start' command: {e}")
        await update.message.reply_text(
            text="An error occurred while processing your request. Please try again later."
        )
start_command_handler = CommandHandler("start", _start)


async def _stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /stop command.
    Sends a goodbye message
    """
    logger.info(f"Received '/stop' command from user: {update.effective_user.name}")
    try:
        # send msg
        await update.message.reply_text(
            text="""
            Sad to see you go!\r\nIf you change your mind, just type /start to begin again.\r\nGoodbye! 👋
            """
        )
    except Exception as e:
        logger.error(f"Error handling '/stop' command: {e}")
        await update.message.reply_text(
            text="An error occurred while processing your request. Please try again later."
        )
stop_command_handler = CommandHandler("stop", _stop)


__all__ = ["start_command_handler", 'stop_command_handler']