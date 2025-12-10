from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.logger import logger

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start Command Handler"""
    # Greeting
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="안녕? 서연이 매니저 김유나야. 서연이 스케줄 관리하느라 바쁘니까 용건만 간단히 해줄래? 😎"
    )
    logger.info(f"🚀 Bot Started by {update.effective_user.id}")
