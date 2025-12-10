import json
import requests
import random
import time
import os
import websocket # standard library in some envs, or pip install websocket-client
import uuid
import urllib.request
import urllib.parse

COMFY_SERVER = "http://127.0.0.1:8188"
WORKFLOW_FILE = "Seoyeon_Flux_v1.json"
OUTPUT_DIR = "comfy_outputs"

# Base Trigger & Quality Prompts (Extracted from JSON)
BASE_PREFIX = "seoyoon, beautiful young Korean woman, "
BASE_SUFFIX = ", (masterpiece:1.25), (best quality:1.25), 8k RAW photo, photorealistic"

def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    try:
        req = urllib.request.Request(f"{COMFY_SERVER}/prompt", data=data)
        return json.loads(urllib.request.urlopen(req).read())
    except Exception as e:
        print(f"❌ ComfyUI Connection Error: {e}")
        return None

def get_history(prompt_id):
    with urllib.request.urlopen(f"{COMFY_SERVER}/history/{prompt_id}") as response:
        return json.loads(response.read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"{COMFY_SERVER}/view?{url_values}") as response:
        return response.read()

def submit_comfy_task(user_prompt):
    """
    Submits a task to ComfyUI and returns the prompt_id immediately.
    """
    print(f"🎨 [ComfyUI] Submitting: {user_prompt[:50]}...")
    
    if not os.path.exists(WORKFLOW_FILE):
        print(f"❌ Workflow file not found: {WORKFLOW_FILE}")
        return None, None

    with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # Inject Prompt (Node 6) & Seed (Node 3)
    full_prompt = f"{BASE_PREFIX} {user_prompt} {BASE_SUFFIX}"
    workflow["6"]["inputs"]["text"] = full_prompt
    
    seed = random.randint(0, 1000000000000)
    workflow["3"]["inputs"]["seed"] = seed

    # Queue Prompt
    response = queue_prompt(workflow)
    if not response:
        return None, None
        
    prompt_id = response['prompt_id']
    print(f"⏳ ComfyUI Task Queued: {prompt_id}")
    return prompt_id, seed

def wait_for_image(prompt_id, seed, timeout=3600):
    """
    Polls for the image completion. Timeout default increased to 1 hour.
    """
    print(f"🕰️ [ComfyUI] Waiting for task {prompt_id}...")
    start_time = time.time()
    
    while (time.time() - start_time) < timeout:
        time.sleep(5) # Poll every 5s
        try:
            history = get_history(prompt_id)
            if prompt_id in history:
                # Task Done
                outputs = history[prompt_id]['outputs']
                if '9' in outputs:
                    images = outputs['9']['images']
                    if images:
                        img_info = images[0]
                        image_data = get_image(img_info['filename'], img_info['subfolder'], img_info['type'])
                        print(f"✅ Image Generated: {img_info['filename']}")
                        
                        if not os.path.exists(OUTPUT_DIR):
                            os.makedirs(OUTPUT_DIR)
                        
                        output_path = os.path.join(OUTPUT_DIR, f"comfy_{prompt_id}.png")
                        with open(output_path, "wb") as f:
                            f.write(image_data)
                            
                        return output_path
                break
        except Exception as e:
            # Ignore connection glitches during long wait
            pass
            
    return None

def generate_comfy_image(user_prompt):
    # Legacy wrapper for blocking call (if needed)
    pid, seed = submit_comfy_task(user_prompt)
    if pid:
        return wait_for_image(pid, seed), seed
    return None, None
