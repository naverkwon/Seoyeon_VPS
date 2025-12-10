import os
import requests
from telegram import Update
from telegram.ext import ContextTypes
from bot.brain.vision import analyze_image, analyze_video
from bot.utils.logger import logger
from bot.brain.imagine import log_to_gallery  # If we want to save user uploaded photos to gallery? Maybe separate function.

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    logger.info(f"📸 [Debug] Handle Photo Triggered (User: {user.id})")

    try:
        # 1. Get File
        if update.message.document:
            file_id = update.message.document.file_id
        else:
            file_id = update.message.photo[-1].file_id
            
        new_file = await context.bot.get_file(file_id)
        
        # 2. Download
        os.makedirs("downloads", exist_ok=True)
        file_path = f"downloads/user_{user.id}_{file_id}.jpg"
        await new_file.download_to_drive(file_path)
        
        user_caption = update.message.caption
        
        # 3. Analyze (Brain)
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        
        result = analyze_image(file_path, user_caption)
        
        response_text = result.get("response", "음... 잘 모르겠어요.")
        insta_caption = result.get("caption")
        insta_tags = result.get("tags")
        
        # 4. Reply
        await context.bot.send_message(chat_id=chat_id, text=response_text)
        
        # [Memory] Save to History
        from bot.utils import file_ops
        
        # Save Visual Description so Brain remembers what was in the photo
        # Response content usually contains "The image features..." 
        # But we need the raw analysis.
        # Let's check `result` dict again.
        visual_desc = result.get("visual_description", result.get("description", "Image Analysis Failed"))
        if not visual_desc or "The image features" not in str(visual_desc):
             # Fallback if specific key missing, though `analyze_image` should return it.
             # Wait, `analyze_image` returns `{"response": ..., "description": ...}`?
             visual_desc = "Visual Content: " + str(result.get("description", "Unknown Image"))
             
        history_input = f"[Photo Sent] Content: {visual_desc} | Caption: {user_caption if user_caption else 'None'}"
        file_ops.save_context_to_history(history_input, response_text)
        
        # Optional: Logging user photos to gallery? 
        # Original code didn't seem to save user photos to public gallery, just logged metadata?
        # Let's save metadata for dashboard analysis.
        # But we need a URL for gallery. We only have local path.
        # Skip gallery logging for now or implement local serving.

    except Exception as e:
        logger.error(f"❌ Photo Handler Error: {e}")
        await context.bot.send_message(chat_id=chat_id, text=f"오빠, 사진이 안 보여요 ㅠ 왜 이러지? ({e})")

async def handle_video_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        video_file = await update.message.video.get_file()
        file_path = f"downloads/video_{update.effective_user.id}.mp4"
        await video_file.download_to_drive(file_path)
        
        await context.bot.send_message(chat_id=chat_id, text="🎥 영상 받고 있어요... 잠시만요!")
        
        result = analyze_video(file_path, update.message.caption)
        await context.bot.send_message(chat_id=chat_id, text=result.get("response"))
        
    except Exception as e:
        logger.error(f"❌ Video Handler Error: {e}")
        await context.bot.send_message(chat_id=chat_id, text="영상 처리에 실패했어요 ㅠ")
