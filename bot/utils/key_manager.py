import time
import itertools
from datetime import datetime, timedelta
from bot import config
from bot.utils.logger import logger

class KeyManager:
    """
    Manages a pool of API keys with state tracking and cooldowns.
    Statuses:
    - ACTIVE: Ready to use.
    - COOLDOWN: Temporarily disabled (Rate Limit).
    - DEAD: Permanently disabled (Invalid Key).
    """
    
    def __init__(self, keys):
        self.keys = {
            k: {"status": "ACTIVE", "cooldown_until": None, "usage_count": 0} 
            for k in keys
        }
        self._cycle = itertools.cycle(keys) if keys else None
        
    def get_valid_key(self):
        """Returns the next ACTIVE key, or None if all are busy/dead."""
        if not self.keys:
            return None
            
        # Try finding an available key (Loop logic to avoid infinite scan)
        checked_count = 0
        total_keys = len(self.keys)
        
        while checked_count < total_keys:
            current_key = next(self._cycle)
            key_data = self.keys[current_key]
            
            # Check Cooldown Expiry
            if key_data["status"] == "COOLDOWN":
                if datetime.now() > key_data["cooldown_until"]:
                    logger.info(f"✅ Key Revived from Cooldown: ...{current_key[-4:]}")
                    key_data["status"] = "ACTIVE"
                    key_data["cooldown_until"] = None
            
            # Return if ACTIVE
            if key_data["status"] == "ACTIVE":
                key_data["usage_count"] += 1
                return current_key
                
            checked_count += 1
            
        logger.warning("⚠️ All API Keys are currently cooling down or dead.")
        return None

    def report_error(self, key, error_type="RATE_LIMIT"):
        """
        Reports an error for a specific key.
        error_type: "RATE_LIMIT" (429) or "INVALID" (400/403)
        """
        if key not in self.keys:
            return

        if error_type == "RATE_LIMIT":
            # Set 1-minute cooldown
            cooldown_time = datetime.now() + timedelta(minutes=1)
            self.keys[key]["status"] = "COOLDOWN"
            self.keys[key]["cooldown_until"] = cooldown_time
            logger.warning(f"⏳ Key Cooldown (quota exceeded): ...{key[-4:]} until {cooldown_time.strftime('%H:%M:%S')}")
            
        elif error_type == "INVALID":
            self.keys[key]["status"] = "DEAD"
            logger.error(f"💀 Key Marked DEAD (Invalid): ...{key[-4:]}")

    def get_status_report(self):
        """Returns a short summary of key statuses."""
        active = sum(1 for v in self.keys.values() if v["status"] == "ACTIVE")
        cooldown = sum(1 for v in self.keys.values() if v["status"] == "COOLDOWN")
        dead = sum(1 for v in self.keys.values() if v["status"] == "DEAD")
        return f"Keys: {active} Active, {cooldown} Cooling, {dead} Dead"

# Global Instance
manager = KeyManager(config.GEMINI_KEYS)
