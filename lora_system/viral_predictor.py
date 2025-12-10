
import random

class ViralPredictor:
    """
    AI Agency Viral Prediction Engine.
    Predicts the potential engagement (Likes/Shares) of a generated image/prompt.
    Uses heuristic analysis of:
    1. Trend keywords (e.g. "cats", "morning routine").
    2. Aesthetic factors (e.g. "golden hour", "bokeh").
    3. Character appeal (e.g. "smile", "eye contact").
    """
    
    VIRAL_FACTORS = {
        'high_value': [
            'golden hour', 'seductive smile', 'direct eye contact', 'cleavage', 
            'cat', 'dog', 'puppy', 'luxury', 'penthouse', 'sports car',
            'wet hair', 'parted lips'
        ],
        'medium_value': [
            'morning', 'coffee', 'cafe', 'workout', 'gym', 'yoga',
            'sunset', 'beach', 'bikini', 'party_dress'
        ],
        'niche_value': [
            'book', 'library', 'rain', 'forest', 'fantasy'
        ]
    }
    
    BASE_ENGAGEMENT = 1500 # Baseline likes for Seoyeon
    
    def __init__(self):
        pass
        
    def predict_engagement(self, prompt, metadata=None):
        """
        Analyze prompt and metadata to predict likes.
        """
        score = 0
        prompt_lower = prompt.lower()
        
        # 1. Keyword Analysis
        hits = []
        
        for kw in self.VIRAL_FACTORS['high_value']:
            if kw in prompt_lower:
                score += random.randint(500, 1000)
                hits.append(kw)
                
        for kw in self.VIRAL_FACTORS['medium_value']:
            if kw in prompt_lower:
                score += random.randint(200, 500)
                hits.append(kw)
        
        # 2. Random Virality (The Algorithm Luck)
        luck_factor = random.uniform(0.8, 1.5)
        
        predicted_likes = int((self.BASE_ENGAGEMENT + score) * luck_factor)
        
        # 3. Generate Analysis Report
        grade = "C"
        if predicted_likes > 10000: grade = "S+"
        elif predicted_likes > 5000: grade = "A"
        elif predicted_likes > 3000: grade = "B"
        
        return {
            'predicted_likes': predicted_likes,
            'grade': grade,
            'viral_factors_found': hits,
            'luck_multiplier': f"{luck_factor:.2f}x"
        }
    
    def suggest_improvements(self, prompt):
        """
        Suggest keywords to boost virality.
        """
        suggestions = []
        prompt_lower = prompt.lower()
        
        if "smile" not in prompt_lower:
            suggestions.append("Add 'seductive smile' or 'bright smile'")
        if "lighting" not in prompt_lower and "golden hour" not in prompt_lower:
            suggestions.append("Change lighting to 'golden hour' or 'cinematic'")
        
        return suggestions
