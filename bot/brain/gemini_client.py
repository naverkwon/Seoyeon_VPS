import google.generativeai as genai
import time
import json
from bot import config
from bot.utils.logger import logger
from bot.utils.key_manager import manager

def get_gemini_model():
    """Returns a GenerativeModel using a VALID key from KeyManager."""
    api_key = manager.get_valid_key()
    if not api_key:
        raise ValueError("No Valid Gemini API Keys available (All dead or cooling down)")
    
    # Transport='rest' is critical to avoid gRPC DNS timeouts
    genai.configure(api_key=api_key, transport="rest")
    return genai.GenerativeModel('gemini-flash-latest'), api_key

def generate_text_safe(prompt):
    """
    Generates text using Gemini with:
    - Intelligent Key Rotation (KeyManager)
    - Retry Logic (Backoff)
    - JSON Fallback
    """
    if not config.GEMINI_KEYS:
        return {"response": "API 키가 설정되지 않았습니다.", "image_prompt": None}

    # Retry limit based on total keys to give fair chance
    max_retries = len(config.GEMINI_KEYS) * 2
    retry_count = 0
    
    while retry_count < max_retries:
        current_key = None
        try:
            model, current_key = get_gemini_model()
            response = model.generate_content(prompt)
            
            # 1. Check for quick accessor error (Blocked content)
            try:
                text = response.text
            except Exception as e:
                # If finish_reason is not STOP, response.text fails
                logger.warning(f"⚠️ Generation Blocked/Failed: {e}")
                raise e # Trigger retry

            # 2. Parse JSON
            text = text.replace("```json", "").replace("```", "").strip()
            try:
                start_idx = text.find('{')
                if start_idx != -1:
                    text_to_parse = text[start_idx:]
                    obj, _ = json.JSONDecoder().raw_decode(text_to_parse)
                    return obj
                else:
                    return json.loads(text) 
            except json.JSONDecodeError:
                logger.warning(f"⚠️ JSON Decode Error. Raw: {text[:100]}... attempting Regex fallback.")
                
                # Regex Fallback
                import re
                
                # Extract Response (Greedy until next quote, handling escaped quotes is hard, but simple is often enough for fallback)
                # Better pattern: look for "response": "(...)" 
                # Handling newlines: dotall needed? Gemini often breaks lines.
                
                response_match = re.search(r'"response"\s*:\s*"(.*?)(?<!\\)"', text, re.DOTALL)
                response_content = response_match.group(1) if response_match else text # Worst case: return raw text
                
                # Cleanup escaped newlines if regex captured them literally
                # content usually comes as literal text.
                
                # Extract Image Prompt
                prompt_match = re.search(r'"image_prompt"\s*:\s*"(.*?)(?<!\\)"', text, re.DOTALL)
                image_prompt = prompt_match.group(1) if prompt_match else None
                
                # Extract Explicit flag
                explicit_match = re.search(r'"is_explicit"\s*:\s*(true|false)', text, re.IGNORECASE)
                is_explicit = explicit_match.group(1).lower() == 'true' if explicit_match else False

                return {
                    "response": response_content,
                    "image_prompt": image_prompt,
                    "is_explicit": is_explicit
                }

        except Exception as e:
            error_msg = str(e)
            
            # Report to Manager
            if "Quota" in error_msg or "429" in error_msg:
                manager.report_error(current_key, "RATE_LIMIT")
            elif "API key not valid" in error_msg:
                manager.report_error(current_key, "INVALID")
            else:
                logger.error(f"❌ Gemini Error: {e}")
                time.sleep(1) # Short wait for generic errors
            
            retry_count += 1
            
    # All retries failed
    logger.error("❌ All Gemini Keys failed.")
    return {"response": "오빠, 나 지금 머리가 좀 아파서... (API Error)", "image_prompt": None}
