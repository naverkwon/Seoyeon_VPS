try:
    import brain_comfy
    print("✅ brain_comfy loaded successfully")
except ImportError as e:
    print(f"❌ Failed to import brain_comfy: {e}")
    exit(1)

import requests

def test_connection():
    url = "http://127.0.0.1:8188/system_stats"
    try:
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            print("✅ ComfyUI Server is ONLINE (Port 8188)")
        else:
            print(f"❌ ComfyUI Server returned {resp.status_code}")
    except Exception as e:
        print(f"❌ ComfyUI Connection Failed: {e}")
        print("💡 Hint: Ensure ComfyUI is running with './python_embeded/python.exe main.py' or similar.")

if __name__ == "__main__":
    test_connection()
