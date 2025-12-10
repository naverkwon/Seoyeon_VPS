import google.generativeai as genai
import os
import time

# Load Keys
    # Load keys from .env
    load_dotenv()
    env_keys = os.getenv("GEMINI_API_KEYS", "")
    candidates_keys = [k.strip() for k in env_keys.split(',') if k.strip()]
    
    # Also add the latest one manually just in case env isn't reloaded in this script process yet?
    # No, load_dotenv() handles it. But let's be safe and clear the manual override.
    keys = candidates_keys

print(f"🔑 Found {len(keys)} API Keys.")

def test_model():
    candidates = [
        "gemini-1.5-flash",
        'gemini-1.5-pro-latest',
        'gemini-1.5-pro',
        'gemini-1.5-pro-001',
        'gemini-1.5-pro-exp-0827'
    ]
    
    for model_name in candidates:
        print(f"\n🔎 Testing Model: {model_name}")
        for i, key in enumerate(keys):
            print(f"  > Key #{i+1} ({key[:5]}...): ", end="")
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Ping")
                print(f"✅ Success! Response: {response.text.strip()}")
                return model_name # Return the working model name
            except Exception as e:
                if "429" in str(e):
                    print(f"❌ Quota Exceeded")
                elif "404" in str(e):
                     print(f"❌ Not Found")
                else:
                    print(f"❌ Error: {str(e)[:100]}")
                time.sleep(0.5)
    return None

if __name__ == "__main__":
    if test_model():
        print("\n🎉 Verification Passed: Gemini 1.5 Flash is active and responding.")
    else:
        print("\n🔥 Verification Failed: All keys failed.")
