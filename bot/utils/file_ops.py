import os
from bot import config
from bot.utils.logger import logger

def load_persona():
    try:
        with open(config.PERSONA_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"❌ Persona Load Error: {e}")
        return "You are Kim Yuna, Seoyeon's manager."

def load_user_profile():
    """오빠(User)의 신상 정보를 로드함"""
    try:
        if os.path.exists(config.USER_PROFILE_FILE):
            with open(config.USER_PROFILE_FILE, 'r', encoding='utf-8') as f:
                return f"[User Profile]\n{f.read()}\n"
        return ""
    except Exception as e:
        logger.error(f"❌ Profile Load Error: {e}")
        return ""

def load_recent_history(limit=10):
    try:
        if not os.path.exists('conversation_log.csv'):
            return ""
            
        import csv
        with open('conversation_log.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)
            
        recent = data[-limit:] 
        history_text = ""
        last_timestamp = None
        
        for row in recent:
            if len(row) >= 3:
                # row[0] = Timestamp, row[1] = User Input, row[2] = Bot Response
                history_text += f"User: {row[1]}\nYou: {row[2]}\n"
                last_timestamp = row[0] # Keep updating to the latest
                
        return f"[Recent Conversation History]\n{history_text}\n", last_timestamp
        
    except Exception as e:
        logger.error(f"❌ History Load Error: {e}")
        return "", None

def save_context_to_history(user_input, bot_response):
    try:
        import csv
        from datetime import datetime
        
        file_exists = os.path.exists('conversation_log.csv')
        
        with open('conversation_log.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "User", "Bot"])
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, user_input, bot_response])
            
    except Exception as e:
        logger.error(f"❌ History Save Error: {e}")
