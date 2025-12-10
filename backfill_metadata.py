import os
import json
import re
import google.generativeai as genai
from seoyeon_bot import get_next_gemini_model, load_persona 

# Constants
IMAGE_DIR = "generated_images"
METADATA_FILE = "gallery_metadata.json"

def generate_vision_caption(image_path):
    """지나간 사진을 보고 캡션 생성"""
    try:
        # Import dynamically to ensure it uses the configured instance
        from seoyeon_bot import get_next_gemini_model
        model = get_next_gemini_model()
        
        # Ensure we are using Flash for vision (Force override if needed, but get_next generates Flash now)
        # seoyeon_bot.py was updated to return gemini-1.5-flash
        
        from PIL import Image
        img = Image.open(image_path)
        
        system_instruction = load_persona()
        prompt = f"""
        {system_instruction}
        
        [Task: Instagram Reconstruction]
        Analyze this photo of Seoyeon.
        
        Action:
        1. Write a cheeky, short Instagram caption (as Seoyeon).
        2. Add 5-7 relevant hashtags.
        3. JSON Output: {{ "caption": "...", "tags": "#..." }}
        """
        
        import time
        
        max_retries = 5
        wait_time = 10
        
        for attempt in range(max_retries):
            try:
                response = model.generate_content([prompt, img])
                text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(text)
                return data.get("caption", "추억 소환 📸"), data.get("tags", "#Seoyeon #Memory")
            except Exception as e:
                if "429" in str(e) or "Quota" in str(e):
                    print(f"⚠️ Quota Hit. Waiting {wait_time}s... (Attempt {attempt+1}/{max_retries})")
                    time.sleep(wait_time)
                    wait_time *= 1.5 # Exponential backoff
                else:
                    raise e
                    
        return "복구 실패 (Quota)", "#Error"
        
    except Exception as e:
        print(f"❌ Vision Error for {image_path}: {e}")
        return "복구된 사진", "#Restored"

def backfill():
    if not os.path.exists(IMAGE_DIR):
        print("No image directory found.")
        return

    # Load existing metadata
    metadata = {}
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            try:
                metadata = json.load(f)
            except:
                pass

    files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(('.jpg', '.png'))]
    print(f"🔍 Found {len(files)} images. Checking metadata...")

    count = 0
    for filename in files:
        # Check if missing OR if it's a failed placeholder
        needs_update = False
        if filename not in metadata:
            needs_update = True
        elif metadata[filename].get("caption") == "복구된 사진":
            needs_update = True
            
        if needs_update:
            print(f"✨ Generating metadata for: {filename}")
            
            # 1. Parse Seed from Filename (bot_gen_xxx_seed123.jpg)
            seed = "Unknown"
            match = re.search(r"seed(\d+)", filename)
            if match:
                seed = int(match.group(1))
            
            # 2. Generate Caption using Vision
            filepath = os.path.join(IMAGE_DIR, filename)
            caption, tags = generate_vision_caption(filepath)
            
            # 3. Save
            metadata[filename] = {
                "prompt": "Restored from Image Analysis", # Prompt lost
                "seed": seed,
                "caption": caption,
                "tags": tags,
                "timestamp": "2024-01-01 00:00:00" # Placeholder or extract from file modified time
            }
            
            # Get real file time if possible
            try:
                mtime = os.path.getmtime(filepath)
                from datetime import datetime
                real_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                metadata[filename]["timestamp"] = real_time
            except:
                pass

            count += 1
            
            # Save progressively
            with open(METADATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"✅ Backfill Complete. Updated {count} images.")

if __name__ == "__main__":
    backfill()
