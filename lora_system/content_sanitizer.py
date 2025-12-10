
import os
import random
import time

# Try importing NudeNet, fallback to Mock if not available
try:
    from nudenet import NudeDetector
    NUDENET_AVAILABLE = True
except ImportError:
    NUDENET_AVAILABLE = False
    print("NudeNet not installed. Using MockSanitizer.")

class ContentSanitizer:
    """
    AI Agency Content Sanitizer Module.
    Responsible for:
    1. Detecting sensitive body parts (using NudeNet).
    2. Blurring/Censoring detected areas (using OpenCV/PIL).
    3. Providing a 'Safety Score' for Instagram/Platform compliance.
    """

    def __init__(self, high_precision=False):
        self.detector = None
        self.high_precision = high_precision
        
        if NUDENET_AVAILABLE:
            # Initialize NudeNet Detector
            # Note: This might download weights on first run
            try:
                model_name = 'base' if not high_precision else 'default'
                self.detector = NudeDetector() # Default usage
                print(f"ContentSanitizer: NudeNet ({model_name}) Loaded.")
            except Exception as e:
                print(f"ContentSanitizer: Error initializing NudeNet: {e}")
                self.detector = None
    
    def analyze_image(self, image_path):
        """
        Analyze an image for unsafe content.
        Returns a list of detections: [{'class': 'exposed_breasts', 'score': 0.9, 'box': [...]}]
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
            
        if self.detector:
            return self.detector.detect(image_path)
        else:
            return self._mock_detect(image_path)

    def is_safe_for_instagram(self, image_path, threshold=0.7):
        """
        Determines if image is safe for general platforms.
        """
        results = self.analyze_image(image_path)
        unsafe_classes = [
            'exposed_breasts', 'exposed_genitalia', 'exposed_anus', 
            'exposed_buttocks', 'erect_penis'
        ]
        
        # Check for bad detection
        detected_unsafe = []
        for det in results:
            if det['class'] in unsafe_classes and det['score'] > threshold:
                detected_unsafe.append(det['class'])
        
        is_safe = len(detected_unsafe) == 0
        return is_safe, detected_unsafe

    def censor_image(self, image_path, output_path=None):
        """
        Detects and blurs unsafe areas.
        """
        # Placeholder for blurring logic (requires OpenCV/PIL)
        # For this prototype, we will just return the analysis
        return self.analyze_image(image_path)
        
    def _mock_detect(self, image_path):
        """
        Simulate detection for testing without NudeNet weights.
        """
        print(f"MockSanitizer: Analyzing {image_path}...")
        time.sleep(0.5) # Simulate processing
        
        # Randomly simulating safety based on filename keywords for testing
        filename = os.path.basename(image_path).lower()
        if "nsfw" in filename or "nude" in filename:
            return [
                {'class': 'exposed_breasts', 'score': 0.95, 'box': [100, 100, 200, 200]},
                {'class': 'exposed_genitalia', 'score': 0.98, 'box': [300, 300, 400, 400]}
            ]
        elif "tease" in filename:
            return [
                {'class': 'exposed_breasts', 'score': 0.45, 'box': [100, 100, 200, 200]} # Low confidence
            ]
        
        return [] # Safe
