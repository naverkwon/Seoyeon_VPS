import csv
import json
import os
import sys
import datetime

# Add parent dir to path to import brain_replicate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import brain_replicate

LOG_FILE = "../conversation_log.csv"
GALLERY_FILE = "../gallery_data.json"

def backfill_gallery():
    print("📂 Starting Gallery Backfill...")
    
    if not os.path.exists(LOG_FILE):
        print("❌ Log file not found.")
        return

    # 1. Read Log
    entries_to_process = []
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) >= 4:
                timestamp, user_msg, bot_msg, img_prompt = row[0], row[1], row[2], row[3]
                if img_prompt and img_prompt != "N/A" and len(img_prompt) > 10:
                    entries_to_process.append({
                        "timestamp": timestamp,
                        "user_context": user_msg,
                        "image_prompt": img_prompt,
                        "image_url": "PLACEHOLDER_URL" # Log doesn't save URL, user must manually update or we just save metadata
                    })
    
    print(f"🔍 Found {len(entries_to_process)} image prompts.")
    
    # 2. Load existing gallery (avoid duplicates)
    existing_prompts = set()
    gallery_data = []
    if os.path.exists(GALLERY_FILE):
        with open(GALLERY_FILE, 'r', encoding='utf-8') as f:
            try:
                gallery_data = json.load(f)
                for item in gallery_data:
                    existing_prompts.add(item.get("image_prompt"))
            except:
                pass

    # 3. Process
    new_count = 0
    for entry in entries_to_process:
        if entry["image_prompt"] in existing_prompts:
            continue
            
        print(f"🎨 Generating Metadata for: {entry['image_prompt'][:30]}...")
        
        meta_prompt = f"""
[Task]
Analyze this image prompt and generate an Instagram caption and hashtags.
Image Prompt: "{entry['image_prompt']}"
Context: K-pop idol Seoyeon's private life.

[Format]
JSON Only:
{{
  "caption": "Short, natural Korean caption (as Seoyeon)",
  "hashtags": "#Seoyeon #Daily #Kpop ..."
}}
"""
        raw_meta = brain_replicate.query_replicate(meta_prompt, "You are a social media manager.")
        
        caption = "Caption Generation Failed"
        tags = "#Seoyeon"
        try:
            import re
            json_match = re.search(r'\{.*\}', raw_meta, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                caption = data.get("caption", caption)
                tags = data.get("hashtags", tags)
        except:
            pass
            
        entry["caption"] = caption
        entry["hashtags"] = tags
        gallery_data.append(entry)
        new_count += 1
        
    # 4. Save
    with open(GALLERY_FILE, 'w', encoding='utf-8') as f:
        json.dump(gallery_data, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Backfill Complete. Added {new_count} new entries to {GALLERY_FILE}")

if __name__ == "__main__":
    backfill_gallery()
