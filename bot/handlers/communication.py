import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot import config
from bot.brain.thinking import think_and_reply
from bot.brain.imagine import hand_generate_image
from bot.handlers.special_features import handle_diary_request, handle_quest_request
from bot.utils.logger import logger

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    user_text = update.message.text
    
    logger.info(f"📨 [Debug] handle_message Called! User: {user.first_name}")
    config.LAST_CHAT_ID = chat_id # Update Global State
    
    # -------------------------------------------------------------------------
    # 1. Special Feature Triggers
    # -------------------------------------------------------------------------
    if any(k in user_text for k in ["일기", "비밀노트", "속마음", "다이어리"]):
        await handle_diary_request(update, context)
        return

    if any(k in user_text for k in ["미션", "도전", "훔쳐", "찍어와", "알아와"]):
        await handle_quest_request(update, context)
        return

    # -------------------------------------------------------------------------
    # 2. Admin Commands
    # -------------------------------------------------------------------------
    if user_text.strip().startswith("/seed"):
        parts = user_text.split()
        if len(parts) > 1:
            if parts[1].lower() == "reset":
                config.FIXED_SEED = None
                await context.bot.send_message(chat_id=chat_id, text="🎲 Seed Reset: Random Mode ON")
            else:
                try:
                    target_seed = int(parts[1])
                    config.FIXED_SEED = target_seed
                    await context.bot.send_message(chat_id=chat_id, text=f"🔒 Seed Locked: {target_seed}\n(이제부터 이 얼굴/구도로만 생성됩니다.)")
                except ValueError:
                    await context.bot.send_message(chat_id=chat_id, text="❌ Invalid Seed Number")
        else:
             await context.bot.send_message(chat_id=chat_id, text=f"🔑 Current Seed: {config.FIXED_SEED if config.FIXED_SEED else 'Random'}")
        return

    # -------------------------------------------------------------------------
    # 3. Brain Processing (Thinking)
    # -------------------------------------------------------------------------
    loop = asyncio.get_running_loop()
    
    # Run CPU-bound/Network-bound thinking in executor to avoid blocking event loop
    result = await loop.run_in_executor(None, think_and_reply, user_text)
    
    if not result:
        await context.bot.send_message(chat_id=chat_id, text="오빠, 지금 통신 보안 걸려서 내용 확인이 안 돼요. 나중에 다시 말해줄래요?")
        return

    # 4. Send Text Response
    response_text = result.get('response', '...')
    await context.bot.send_message(chat_id=chat_id, text=response_text)
    
    # [Memory] Save to History
    from bot.utils import file_ops
    file_ops.save_context_to_history(user_text, response_text)

    # -------------------------------------------------------------------------
    # 5. Image Generation (If requested)
    # -------------------------------------------------------------------------
    image_prompt = result.get('image_prompt')
    is_explicit = result.get('is_explicit', False)

    if image_prompt:
        # Normalize to list
        prompt_list = image_prompt if isinstance(image_prompt, list) else [image_prompt]
        
        for idx, single_prompt in enumerate(prompt_list):
            clean_prompt = single_prompt.strip().strip("'").strip('"')
            
            # [A] Explicit Mode -> Send Prompt Only
            if is_explicit:
                prefix = f"📝 **[주문서 {idx+1}]**\n" if len(prompt_list) > 1 else ""
                await context.bot.send_message(chat_id=chat_id, text=f"{prefix}{clean_prompt}")
                continue 
                
            # [B] Normal Mode -> Generate Image
            msg = f"사진({idx+1}/{len(prompt_list)}) 보내는 중... 🔄" if len(prompt_list) > 1 else "사진 보내는 중... 🔄"
            await context.bot.send_message(chat_id=chat_id, text=msg)
            
            # Hand Generate (blocking, so run in executor if needed, but requests handles it)
            # To be safe, run generation in executor too
            try:
                # Need a wrapper for executor
                def gen_wrapper():
                    return hand_generate_image(clean_prompt)
                
                image_url, seed, caption, tags = await loop.run_in_executor(None, gen_wrapper)
                
                if image_url:
                    caption_text = f"{caption}\n\n{tags}" if caption else ""
                    await context.bot.send_photo(chat_id=chat_id, photo=image_url, caption=caption_text)
                    if seed:
                         await context.bot.send_message(chat_id=chat_id, text=f"Seed: {seed}")
                else:
                    await context.bot.send_message(chat_id=chat_id, text="사진 생성을 못했어요 ㅠㅠ (서버 오류)")
                    
            except Exception as e:
                logger.error(f"Generate Error: {e}")
                await context.bot.send_message(chat_id=chat_id, text="사진 생성 실패...")
