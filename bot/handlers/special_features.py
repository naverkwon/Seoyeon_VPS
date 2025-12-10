import random
import time
import json
from telegram import Update
from telegram.ext import ContextTypes
from bot.brain.gemini_client import get_gemini_model
from bot.brain.imagine import hand_generate_image
from bot.utils import file_ops
from bot.utils.logger import logger

# -------------------------------------------------------------------------
# [Feature] Secret Diary
# -------------------------------------------------------------------------
async def handle_diary_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """일기장 훔쳐보기 요청 처리"""
    chat_id = update.effective_chat.id
    
    # Pre-action Message
    pre_msgs = [
        "잠시만요, 서연이 지금 샤워하러 들어갔어요. 아이패드 훔쳐볼게요...",
        "쉿, 서연이 자고 있어서 몰래 서랍 열어보고 있어요...",
        "비밀번호 풀었어요! 대박... 이거 오빠한테만 보여주는 거예요."
    ]
    await context.bot.send_message(chat_id=chat_id, text=random.choice(pre_msgs))
    time.sleep(2) 
    
    system_instruction = file_ops.load_persona()
    prompt = f"""
    {system_instruction}
    
    [Command: Secret Diary Check]
    User wants to see Seoyeon's private diary/thoughts.
    
    Action:
    1. Write a short, secretive diary entry (as Seoyeon).
    2. Themes: Obsession with Min-jun, Secret attraction to Manager(User), or Stress.
    3. JSON Output with 'image_prompt' for a handwritten note or iPad screen.
    """
    
    try:
        model, _ = get_gemini_model()
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        
        diary_content = data.get("response")
        image_prompt = data.get("image_prompt")
        
        # Diary Content Format
        formatted_msg = f"📖 **[서연의 비밀 일기장]**\n\n{diary_content}"
        await context.bot.send_message(chat_id=chat_id, text=formatted_msg, parse_mode="Markdown")
        
        if image_prompt:
             await context.bot.send_message(chat_id=chat_id, text="사진(증거) 보내는 중... 📸")
             image_url, seed, caption, tags = hand_generate_image(image_prompt)
             if image_url:
                 caption_text = f"{caption}\n\n{tags}" if caption else ""
                 await context.bot.send_photo(chat_id=chat_id, photo=image_url, caption=caption_text)
                 
    except Exception as e:
        logger.error(f"❌ Diary Error: {e}")
        await context.bot.send_message(chat_id=chat_id, text="앗, 서연이가 갑자기 나오는 바람에 못 봤어요 ㅠ 나중에 다시 시도해주세요.")

# -------------------------------------------------------------------------
# [Feature] Quest System
# -------------------------------------------------------------------------
async def handle_quest_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """위험한 미션(도촬, 절도 등) 처리"""
    chat_id = update.effective_chat.id
    
    # 1. 긴장감 조성
    await context.bot.send_message(chat_id=chat_id, text="🎲 오빠, 그거 진짜 위험한데... 걸리면 저 죽어요. 일단 해볼게요. (두근두근)")
    time.sleep(2) 
    
    # 2. 주사위 굴리기 (성공 확률 50%)
    success_chance = 0.5
    is_success = random.random() < success_chance
    
    status = "SUCCESS" if is_success else "FAILURE"
    logger.info(f"🎲 Quest Result: {status}")

    system_instruction = file_ops.load_persona()
    prompt = f"""
    {system_instruction}
    
    [Command: Risky Mission]
    User ordered a risky mission (e.g., stealing phone, peeking, recording).
    
    Result: {status}
    
    Action:
    1. If SUCCESS: Boast about the achievement and provide the 'Evidence' (Image/Info). (Excited, Adrenaline)
    2. If FAILURE: Complain that Seoyeon almost caught you. Refuse to provide image. (Scared, Annoyed at User)
    3. JSON Output. 'image_prompt' should be NULL if FAILURE.
    """
    
    try:
        model, _ = get_gemini_model()
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        
        reply_text = data.get("response")
        image_prompt = data.get("image_prompt")
        
        # Result Message
        icon = "🎉" if is_success else "🚨"
        formatted_msg = f"{icon} **[미션 결과: {status}]**\n\n{reply_text}"
        await context.bot.send_message(chat_id=chat_id, text=formatted_msg, parse_mode="Markdown")
        
        if is_success and image_prompt:
             await context.bot.send_message(chat_id=chat_id, text="보상(증거) 보내는 중... 🎁")
             image_url, seed, caption, tags = hand_generate_image(image_prompt)
             if image_url:
                 caption_text = f"{caption}\n\n{tags}" if caption else ""
                 await context.bot.send_photo(chat_id=chat_id, photo=image_url, caption=caption_text)
                 
    except Exception as e:
        logger.error(f"❌ Quest Error: {e}")
        await context.bot.send_message(chat_id=chat_id, text="⚠ 미션 수행 중 오류 발생. 다음에 다시 시도해주세요.")
