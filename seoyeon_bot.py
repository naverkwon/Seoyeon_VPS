import sys
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Import new modular structure
from bot import config
from bot.handlers import commands, communication, media
from bot.utils.logger import logger

def main():
    # 1. Verification
    if not config.TELEGRAM_TOKEN:
        logger.error("Error: 텔레그램 토큰이 없습니다. .env 파일을 확인해주세요.")
        sys.exit(1)
        
    logger.info("🤖 김유나(서연 매니저) 봇 시작 준비 중... (Modular Ver.)")
    
    # 2. Builder
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    
    # 3. Handlers
    # Command Handlers
    application.add_handler(CommandHandler('start', commands.start))
    
    # Text Messages
    # Filters: Text & Not Command
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), communication.handle_message))
    # Media Handlers
    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, media.handle_photo))
    application.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, media.handle_video_msg))
    
    # 4. Run
    logger.info("✅ 봇이 성공적으로 로드되었습니다. 폴링 시작!")
    application.run_polling()

if __name__ == '__main__':
    main()
