from dotenv import load_dotenv
import os

load_dotenv()
keys = os.getenv("GEMINI_API_KEYS", "")
if not keys:
    # Fallback to single key
    single = os.getenv("GEMINI_API_KEY")
    key_list = [single] if single else []
else:
    key_list = [k.strip() for k in keys.split(",") if k.strip()]

print(f"Total Keys Found: {len(key_list)}")
for i, k in enumerate(key_list):
    print(f"Key {i+1}: ...{k[-4:]}")
