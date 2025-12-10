
import requests
import json

BASE_URL = "http://127.0.0.1:5002/api/generate-prompt"

def test_payload(name, payload):
    print(f"Testing {name} ... ", end="")
    try:
        r = requests.post(BASE_URL, json=payload, timeout=5)
        if r.status_code == 200:
            print("OK")
        else:
            print(f"FAIL ({r.status_code})")
            print(r.text[:200])
    except Exception as e:
        print(f"ERROR: {e}")

# 1. Normal
test_payload("Normal", {
    "mode": "auto",
    "character_id": "seoyeon",
    "level": "sfw",
    "category": "general",
    "count": 1
})

# 2. Missing Character ID (Frontend 'selectedChar' issue?)
test_payload("Missing Char ID", {
    "mode": "auto",
    "character_id": None, 
    "level": "sfw",
    "category": "general",
    "count": 1
})

# 3. Missing Level (Frontend null level?)
test_payload("Missing Level", {
    "mode": "auto",
    "character_id": "seoyeon",
    "level": None,
    "category": "general",
    "count": 1
})

# 4. Empty Male ID in With Male (Logic Fix Verification)
test_payload("Empty Male ID", {
    "mode": "builder",
    "character_id": "seoyeon",
    "level": "nsfw",
    "category": "with_male", # With Male
    "male_character": "",   # Empty
    "count": 1
})
