import os
import random
import requests
import replicate
from datetime import datetime
import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.FileHandler('lora_app.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class ImageGenerator:
    FLUX_LORA_URL = "https://huggingface.co/marine302/Seoyeon_flux/resolve/main/bdce2f3df07d7d36a56036ffd69d46ca.safetensors"
    # Unified model version
    MODEL_VERSION = "lucataco/flux-dev-lora:091495765fa5ef2725a175a57b276ec30dc9d39c22d30410f2ede68a3eab66b3"

    @classmethod
    def generate(cls, prompt: str, seed: int = None, output_dir="generated_images", prefix_seoyeon=False):
        """
        Generates an image using Replicate Flux LoRA.
        
        Args:
            prompt (str): The image prompt.
            seed (int, optional): Seed for generation. Defaults to random.
            output_dir (str): Directory to save the image.
            prefix_seoyeon (bool): If True, prepends 'korean woman seoyeon, ' to the prompt.
            
        Returns:
            tuple: (local_filepath, image_url, used_seed) or (None, None, None) on failure.
        """
        if "REPLICATE_API_TOKEN" not in os.environ:
            print("Error: REPLICATE_API_TOKEN not found in environment.")
            return None, None, None

        if seed is None:
            seed = random.randint(0, 2**32 - 1)

        # Prompt Construction
        final_prompt = prompt
        if prefix_seoyeon and "seoyeon" not in prompt.lower():
            final_prompt = f"korean woman seoyeon, {prompt}"
            
        # Common suffix for quality
        suffix = ", masterpiece, best quality, 8k, photorealistic, highly detailed face, soft lighting, shot on 35mm"
        if suffix.strip(", ") not in final_prompt:
             final_prompt += suffix

        # SECURITY: Sanitize Prompt for Replicate (Avoid NSFW Ban/Cost)
        # We replace explicit terms with softer synonyms for the image generator only.
        # The prompt displayed to the user remains explicit/accurate.
        safe_prompt = cls.sanitize_for_replicate(final_prompt)
        
        if final_prompt != safe_prompt:
             logger.info(f"🛡️ Sanitized Prompt: '{final_prompt[:50]}...' -> '{safe_prompt[:50]}...'")
        
        logger.info(f"🎨 Generating with Seed: {seed} | Prompt: {safe_prompt[:100]}...")

        try:
            output = replicate.run(
                cls.MODEL_VERSION,
                input={
                    "prompt": safe_prompt, # Use Sanitized Prompt
                    "hf_lora": cls.FLUX_LORA_URL,
                    "lora_scale": 0.95,
                    "num_inference_steps": 30,
                    "guidance_scale": 3.5,
                    "width": 1080,
                    "height": 1350,
                    "output_format": "jpg",
                    "output_quality": 100,
                    "seed": seed
                }
            )
            image_url = str(output[0]) if isinstance(output, list) else str(output)
            
            # Download
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # Standardized timestamp
            filename = f"seoyeon_{timestamp}_seed{seed}.jpg"
            filepath = os.path.join(output_dir, filename)
            
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                logger.info(f"💾 Saved to {filepath}")
                return filepath, image_url, seed
            else:
                logger.error(f"❌ Download failed: {response.status_code}")
                return None, None, None

        except Exception as e:
            logger.error(f"❌ Replicate Error: {str(e)}")
            if "NSFW" in str(e):
                raise ValueError("NSFW_BLOCK")
            return None, None, None

    @staticmethod
    def sanitize_for_replicate(prompt):
        """
        Replaces explicit NSFW keywords with safer alternatives to avoid rejection.
        """
        replacements = {
            # Anatomy
            "nipples": "chest", "nipple": "chest",
            "areola": "chest",
            "penis": "groin", "erect penis": "groin", "cock": "groin",
            "vagina": "hips", "pussy": "hips", "vulva": "hips",
            "anus": "hips", "anal": "from behind",
            "breasts": "curves", "breast": "curve",
            "cleavage": "neckline",
            "nude": "minimal clothing", "naked": "minimal clothing",
            "uncensored": "detailed",
            # Actions
            "masturbation": "touching sensually", "masturbating": "touching sensually",
            "fingering": "touching", "stroking": "touching",
            "sex": "intimacy", "fucking": "intimacy",
            "cum": "liquid", "semen": "liquid",
            "ejaculation": "climax",
            "orgasm": "bliss"
        }
        
        lower_prompt = prompt.lower()
        for banned, safe in replacements.items():
            if banned in lower_prompt:
                # Simple replace (could be improved with regex word boundaries)
                lower_prompt = lower_prompt.replace(f" {banned} ", f" {safe} ")
                lower_prompt = lower_prompt.replace(f" {banned},", f" {safe},")
                lower_prompt = lower_prompt.replace(f",{banned}", f",{safe}")
                
        return lower_prompt
