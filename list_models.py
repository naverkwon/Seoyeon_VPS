import google.generativeai as genai

# Test Key
api_key = "AIzaSyA6PhBx8lPGiiwnfXX_ShucfVscgFkSReg"

genai.configure(api_key=api_key)

print("🔍 Listing available models for this key...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Found: {m.name}")
except Exception as e:
    print(f"❌ Error listing models: {e}")
