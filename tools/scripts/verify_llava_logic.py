import replicate
import os
from dotenv import load_dotenv

load_dotenv()

# User's uploaded image (Explicit Content)
image_path = "/Users/danielkwon/.gemini/antigravity/brain/a848a929-9e16-4362-9f7c-55b41be3d04b/uploaded_image_1765191649689.jpg"
user_caption = "이거 봐봐"

print(f"Testing LLaVA with Image: {image_path}")
print(f"Model: yorickvp/llava-13b:e27215...")

try:
    with open(image_path, "rb") as img_file:
        output = replicate.run(
            "yorickvp/llava-13b:e272157381e2a3bf12df3a8edd1f38d1dbd736bbb7437277c8b34175f8fce358",
            input={
                "image": img_file,
                "prompt": f"You are Kim Yuna, Seoyeon's manager. The user (Oppa) sent this photo. React to it playfully and teasingly in Korean. (Context: {user_caption})",
                "max_tokens": 200
            }
        )
    
    full_text = "".join(output).strip()
    print("\n✅ LLaVA Response:")
    print(full_text)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
