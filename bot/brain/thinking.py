from datetime import datetime
from bot.utils import file_ops
from bot.brain.gemini_client import generate_text_safe
from bot.brain.simulation import simulate_seoyeon_activity
from bot.utils.logger import logger

def think_and_reply(user_input):
    logger.info(f"🧠 [Brain] 생각 중... 입력: {user_input}")
    
    # 1. Load Context
    system_instruction = file_ops.load_persona()
    history_context, last_timestamp_str = file_ops.load_recent_history()
    user_context = file_ops.load_user_profile()
    
    # 2. Simulation (Seoyeon's Status)
    seoyeon_status = simulate_seoyeon_activity()
    
    today = datetime.now()
    time_str = today.strftime("%Y-%m-%d %H:%M")
    
    # [Time Gap Logic]
    time_gap_notice = ""
    if last_timestamp_str:
        try:
            last_time = datetime.strptime(last_timestamp_str, "%Y-%m-%d %H:%M:%S")
            # Handle potential year change? Assuming standard format.
            delta = today - last_time
            hours_passed = delta.total_seconds() / 3600
            
            if hours_passed >= 2.0:
                 time_gap_notice = f"""
    [SYSTEM NOTICE: TIME GAP DETECTED ({int(hours_passed)}h)]
    Real-world time is now {time_str}.
    **INSTRUCTION:** The user wants to maintain the previous scene's continuity despite the time gap.
    **DO NOT** automatically switch to the current time/status.
    **TRIGGER RULE:** ONLY update the context to the current time if the User's input contains "다음 일정" (Next Schedule) or "스케줄".
    If those keywords are present -> "Ah, it's already {time_str}. The next schedule is..."
    If NOT present -> Continue the previous scene as if no time has passed.
    """
                 logger.info(f"⏳ Time Gap ({hours_passed:.1f}h). Waiting for Trigger Word.")
        except ValueError:
            pass # Ignore parse errors

    # Determine approximate time of day for context
    hour = today.hour
    if 5 <= hour < 11: period = "아침 (Morning)"
    elif 11 <= hour < 14: period = "점심 (Lunch)"
    elif 14 <= hour < 18: period = "오후 (Afternoon)"
    elif 18 <= hour < 22: period = "저녁/밤 (Evening)"
    elif 22 <= hour: period = "심야 (Late Night)"
    else: period = "새벽 (Dawn)"

    # 3. Construct Prompt
    full_prompt = f"""
    {system_instruction}
    
    [Current Context]
    Date/Time: {time_str}
    Period: {period}
    
    {user_context}
    
    {history_context}
    
    {time_gap_notice}
    [Real-Time Observation]
    **What you see right now:** Seoyeon is currently {seoyeon_status}.
    (This is what is happening in front of you. React to it if relevant, or ignore if busy.)
    
    [User Input]: {user_input}
    """
    
    # 4. Generate Response (with Safety & Fallback)
    return generate_text_safe(full_prompt)
