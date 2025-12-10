from dotenv import load_dotenv
import os

load_dotenv()

raw_keys = os.getenv("GEMINI_API_KEYS", "")
if not raw_keys:
    single_key = os.getenv("GEMINI_API_KEY", "")
    keys = [single_key] if single_key else []
else:
    keys = [k.strip() for k in raw_keys.split(",") if k.strip()]

print(f"Total Keys Loaded: {len(keys)}")
for i, k in enumerate(keys):
    masked = f"{k[:4]}...{k[-4:]}" if len(k) > 8 else "INVALID"
    print(f"Key {i+1}: {masked}")
