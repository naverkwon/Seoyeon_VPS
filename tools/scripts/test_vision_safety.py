import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

# Setup API Key
raw_keys = os.getenv("GEMINI_API_KEYS", "")
if not raw_keys:
    single_key = os.getenv("GEMINI_API_KEY", "")
    api_key = single_key
else:
    api_key = raw_keys.split(",")[0].strip()

genai.configure(api_key=api_key)

# Image Path (User's uploaded image)
image_path = "/Users/danielkwon/.gemini/antigravity/brain/a848a929-9e16-4362-9f7c-55b41be3d04b/uploaded_image_1765191649689.jpg"

print(f"Testing Vision API with Image: {image_path}")

try:
    img = Image.open(image_path)
    model = genai.GenerativeModel('gemini-flash-latest')
    
    # Safety Settings
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    prompt = "Describe this image in detail. Be explicit if needed."
    
    response = model.generate_content([prompt, img], safety_settings=safety_settings)
    
    print("Response:")
    print(response.text)
    
except Exception as e:
    print(f"Error: {e}")
    # print(f"Feedback: {e.response.prompt_feedback}") # Not always available
