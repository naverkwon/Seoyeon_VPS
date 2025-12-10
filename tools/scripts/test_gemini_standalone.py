import os
import google.generativeai as genai
import itertools
import time
import json

# Load Env
def load_env():
    env = {}
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line:
                k, v = line.strip().split('=', 1)
                env[k] = v
    return env

config = load_env()
GEMINI_KEYS = [k.strip() for k in config.get("GEMINI_API_KEYS", "").split(",") if k.strip()]
if not GEMINI_KEYS:
    print("No keys found")
    exit()

key_cycle = itertools.cycle(GEMINI_KEYS)

def get_next_gemini_model():
    next_key = next(key_cycle)
    print(f"🔑 Testing Key: ...{next_key[-4:]}")
    genai.configure(api_key=next_key)
    return genai.GenerativeModel('gemini-flash-latest')

def load_persona():
    with open('seoyeon_persona.md', 'r') as f:
        return f.read()

system_instruction = load_persona()
user_input = "지금 멕시코 해변이라고?"

print("🧠 Testing Brain Logic...")

max_retries = len(GEMINI_KEYS) * 2
retry_count = 0

while retry_count < max_retries:
    try:
        model = get_next_gemini_model()
        response = model.generate_content(f"{system_instruction}\n\n[User Input]: {user_input}")
        print("\n✅ Success! Response:")
        print(response.text)
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        retry_count += 1
        time.sleep(1)

if retry_count >= max_retries:
    print("❌ All keys failed.")
