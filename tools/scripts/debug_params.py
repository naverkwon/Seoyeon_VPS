
import requests
import json
import random

BASE_URL = "http://127.0.0.1:5002/api/generate-prompt"

def test_gen(name, payload):
    print(f"--- Testing {name} ---")
    try:
        resp = requests.post(BASE_URL, json=payload, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            prompts = data.get('prompts', [])
            if prompts:
                p_text = prompts[0]['positive']
                print(f"Success. Length: {len(p_text)}")
                print(f"Snippet: {p_text[:100]}...")
                return p_text
            else:
                print("Success but no prompts returned.")
        else:
            print(f"Failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Error: {e}")
    return ""

# 1. Test Level Change
p_sfw = test_gen("SFW Level", {"level": "sfw", "count": 1, "character_id": "seoyeon"})
p_nsfw = test_gen("NSFW Level", {"level": "nsfw_extreme", "count": 1, "character_id": "seoyeon"})

if "nsfw" in p_nsfw.lower() or "topless" in p_nsfw.lower() or "nipple" in p_nsfw.lower():
    print("✅ NSFW content detected in output.")
else:
    print("⚠️ Warning: NSFW content NOT detected in NSFW level output (might be random).")

# 2. Test Character Change (assuming 'jun' exists or another char)
# querying existing chars first
try:
    c_resp = requests.get("http://127.0.0.1:5002/api/characters")
    chars = c_resp.json().get('characters', [])
    char_ids = [c['id'] for c in chars]
    print(f"Available Chars: {char_ids}")
    
    if len(char_ids) > 1:
        other_char = char_ids[1] if char_ids[0] == 'seoyeon' else char_ids[0]
        p_char = test_gen(f"Character: {other_char}", {"level": "sfw", "count": 1, "character_id": other_char})
        
        if other_char in p_char: # assuming trigger word is ID or similar
            print(f"✅ Character ID '{other_char}' found in prompt.")
        else:
            print(f"⚠️ Character ID '{other_char}' NOT clearly found in prompt (might use trigger word).")
except Exception as e:
    print(f"Error fetching chars: {e}")
