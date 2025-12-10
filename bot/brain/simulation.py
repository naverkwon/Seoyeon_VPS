from datetime import datetime
from bot.brain.gemini_client import get_gemini_model
from bot.utils import file_ops
from bot.utils.logger import logger

SEOYEON_STATUS_CACHE = {
    "status": None,
    "timestamp": None
}

def simulate_seoyeon_activity():
    # Check Cache (10 min)
    if SEOYEON_STATUS_CACHE["status"] and SEOYEON_STATUS_CACHE["timestamp"]:
        elapsed = datetime.now() - SEOYEON_STATUS_CACHE["timestamp"]
        if elapsed.total_seconds() < 600:
            return SEOYEON_STATUS_CACHE["status"]

    # [Quota Saving Mode] API Check Disabled
    return "스케줄 소화 중 (API 절약 모드)"

    # --- API Logic (Disabled) ---
    # try:
    #     idol_persona = file_ops.load_persona() # Technically needs seoyeon private persona
    #     current_time = datetime.now().strftime("%H:%M")
    #     hour = datetime.now().hour
    #     
    #     prompt = f"""
    #     {idol_persona}
    #     [Current Time]: {current_time} ({hour}시)
    #     Task: Describe what she is doing RIGHT NOW (1 sentence).
    #     """
    #     
    #     model, _ = get_gemini_model()
    #     response = model.generate_content(prompt)
    #     status = response.text.strip()
    #     
    #     SEOYEON_STATUS_CACHE["status"] = status
    #     SEOYEON_STATUS_CACHE["timestamp"] = datetime.now()
    #     return status
    #     
    # except Exception as e:
    #     logger.error(f"❌ Simulation Error: {e}")
    #     return "스케줄 소화 중"
