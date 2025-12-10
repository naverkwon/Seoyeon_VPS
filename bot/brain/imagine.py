import os
import json
import random
import requests
import asyncio
from datetime import datetime
from bot import config
from bot.utils.logger import logger
from services.image_gen import ImageGenerator
from bot.brain.gemini_client import generate_text_safe

def log_to_gallery(image_prompt, image_url, user_prompt=""):
    """
    Saves generated image metadata to gallery_data.json.
    Includes auto-generated Instagram caption/tags via Replicate.
    """
    try:
        # Generate Caption (Using Gemini Brain)
        try:
            # Simple prompt for caption
            prompt = f"Create a short, aesthetic Instagram caption (Korean) and tags for this image prompt: '{image_prompt}'"
            result = generate_text_safe(prompt)
            caption = result.get("response", "...") or str(result)
            tags = "#Seoyeon #Daily" # Placeholder
        except Exception:
             caption = "..."
             tags = "#Seoyeon"

        # Append new entry
        entry = {
            "timestamp": datetime.now().isoformat(),
            "image_url": image_url,
            "image_prompt": image_prompt,
            "user_context": user_prompt,
            "caption": caption,
            "hashtags": tags
        }
        
        gallery = []
        if os.path.exists(config.GALLERY_FILE):
             with open(config.GALLERY_FILE, "r", encoding="utf-8") as f:
                 try:
                     gallery = json.load(f)
                 except: gallery = []
        
        gallery.append(entry)
        
        with open(config.GALLERY_FILE, "w", encoding="utf-8") as f:
            json.dump(gallery, f, ensure_ascii=False, indent=2)
            
        logger.info(f"📸 Gallery Logged: {len(gallery)} items.")
        return caption, tags
        
    except Exception as e:
        logger.error(f"❌ Gallery Log Error: {e}")
        return None, None

def hand_generate_image(image_prompt):
    logger.info(f"🎨 [Hand] 그리는 중... 프롬프트: {image_prompt[:30]}...")
    
    try:
        # Use Shared Service (Flux LoRA) via services.image_gen
        # Note: seoyeon_bot.py imported imported ImageGenerator which handles Replicate logic
        
        # We need to make sure ImageGenerator is available or reimplement it here.
        # Ideally, we key off the env/config.
        
        seed = config.FIXED_SEED if config.FIXED_SEED else None
        
        image_path, image_url, used_seed = ImageGenerator.generate(image_prompt, seed=seed)
        
        if not image_url:
             return None, None, None, None

        logger.info(f"✅ Image Generated: {image_url}")
        
        # Log to Gallery (Captioning)
        caption, tags = log_to_gallery(image_prompt, image_url, "")
        return image_url, used_seed, caption, tags
        
    except Exception as e:
        logger.error(f"❌ Image Gen Error: {e}")
        if "NSFW" in str(e):
            raise ValueError("NSFW_BLOCK")
        return None, None, None, None
