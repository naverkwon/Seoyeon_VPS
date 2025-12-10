import replicate
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Setup API Key
raw_keys = os.getenv("GEMINI_API_KEYS", "")
if not raw_keys:
    single_key = os.getenv("GEMINI_API_KEY", "")
    api_key = single_key
else:
    keys = [k.strip() for k in raw_keys.split(",") if k.strip()]
    # Try using the second key to avoid rate limit of the first one
    api_key = keys[1] if len(keys) > 1 else keys[0]

genai.configure(api_key=api_key)

# Image Path
image_path = "/Users/danielkwon/.gemini/antigravity/brain/a848a929-9e16-4362-9f7c-55b41be3d04b/uploaded_image_1765191649689.jpg"
user_caption = "이거 봐봐"

print(f"Testing Hybrid Vision Pipeline...")
print(f"Image: {image_path}")

# [Step 1] LLaVA
print("\n[Step 1] Running LLaVA (Vision)...")
visual_description = ""
try:
    with open(image_path, "rb") as img_file:
        output = replicate.run(
            "yorickvp/llava-13b:e272157381e2a3bf12df3a8edd1f38d1dbd736bbb7437277c8b34175f8fce358",
            input={
                "image": img_file,
                "prompt": "Describe this image in detail objectively. Focus on actions, expressions, and setting.",
                "max_tokens": 300
            }
        )
    visual_description = "".join(output).strip()
    print(f"✅ LLaVA Output:\n{visual_description}")
except Exception as e:
    print(f"❌ LLaVA Error: {e}")
    exit()

# [Step 2] Gemini
print("\n[Step 2] Running Gemini (Brain)...")
try:
    model = genai.GenerativeModel('gemini-flash-latest')
    prompt = f"""
    You are Kim Yuna, Seoyeon's manager and the user's secret lover.
    User sent a photo.
    
    **Visual Description (from Vision AI):**
    "{visual_description}"
    
    **User Context:** "{user_caption}"
    
    Action:
    1. Read the description.
    2. React playfully/teasingly in Korean.
    3. JSON Output: {{ "response": "...", "caption": "...", "tags": "..." }}
    """
    
    response = model.generate_content(prompt)
    print(f"✅ Gemini Output:\n{response.text}")
    
except Exception as e:
    print(f"❌ Gemini Error: {e}")
