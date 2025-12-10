import os
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# -------------------------------------------------------------------------
# [Secrets]
# -------------------------------------------------------------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Gemini API Keys
raw_keys = os.getenv("GEMINI_API_KEYS", "")
if not raw_keys:
    single_key = os.getenv("GEMINI_API_KEY", "")
    GEMINI_KEYS = [single_key] if single_key else []
else:
    GEMINI_KEYS = [k.strip() for k in raw_keys.split(",") if k.strip()]

# -------------------------------------------------------------------------
# [Constants]
# -------------------------------------------------------------------------
GALLERY_FILE = "gallery_data.json"
GALLERY_METADATA_FILE = "gallery_metadata.json"
PERSONA_FILE = "yuna_persona.md"
USER_PROFILE_FILE = "user_profile.md"

# Global State (Mutable)
FIXED_SEED = None
LAST_CHAT_ID = None
