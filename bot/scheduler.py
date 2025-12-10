from datetime import datetime, timedelta
import random
from telegram.ext import ContextTypes
from bot.brain.gemini_client import get_gemini_model
from bot.utils import file_ops
from bot.utils.logger import logger

class IdolScheduler:
    def __init__(self):
        # 07:00 ~ 02:00 (Activity Time)
        self.schedule_map = {
            "MORNING": (7, 10),
            "WORK": (10, 18), 
            "EVENING": (18, 22),
            "NIGHT": (22, 2)
        }
    
    def get_current_status(self):
        hour = datetime.now().hour
        if 7 <= hour < 10: return "MORNING"
        elif 10 <= hour < 18: return "WORK"
        elif 18 <= hour < 22: return "EVENING"
        elif 22 <= hour or hour < 2: return "NIGHT"
        return "SLEEP"

scheduler = IdolScheduler()

async def active_push_job(context: ContextTypes.DEFAULT_TYPE):
    """
    주기적으로 실행되어 유나의 선톡을 유발함.
    """
    # Disable global check for now if needed, or controlled by calling code
    # logger.info("⏰ Scheduler Check...")
    
    try:
        # Probability Check (Example: 5% chance every 10 min)
        if random.random() > 0.05:
            return

        chat_id = context.job.chat_id # Passed via job data or hardcoded/global if single user
        if not chat_id:
             return

        today_status = scheduler.get_current_status()
        if today_status == "SLEEP":
            return

        # Generate Message
        system_instruction = file_ops.load_persona()
        prompt = f"""
        {system_instruction}
        Status: {today_status}
        Task: Inititate conversation with User likely based on current status.
        """
        
        # model, _ = get_gemini_model()
        # response = model.generate_content(prompt)
        # await context.bot.send_message(chat_id=chat_id, text=response.text)
        
    except Exception as e:
        logger.error(f"Scheduler Error: {e}")
