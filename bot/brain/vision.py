import replicate
from PIL import Image
from bot import config
from bot.brain.gemini_client import get_gemini_model
from bot.utils import file_ops
from bot.utils.logger import logger

def analyze_image(image_path, user_caption=None):
    logger.info(f"👁️ [Brain] 이미지 분석 중... (Engine: Hybrid LLaVA + Gemini)")
    
    # 1. LLaVA (Vision) - Get Objective Description
    try:
        # Replicate requires public URL or file handle. Assume file path for now.
        input_data = {
            "image": open(image_path, "rb"),
            "top_p": 1,
            "prompt": "Describe this image in extreme detail, including any people, their clothing, actions, setting, and potential NSFW elements. Be objective.",
            "max_tokens": 1024,
            "temperature": 0.2
        }
        
        output = replicate.run(
            "yorickvp/llava-13b:80537f9eead1a5bfa72d5ac6ea6414379be41d4d4f6679fd776e9535d1eb58bb",
            input=input_data
        )
        visual_description = "".join(output)
        logger.info(f"✅ LLaVA Description: {visual_description[:50]}...")
        
    except Exception as e:
        logger.error(f"❌ LLaVA Error: {e}")
        visual_description = "(Image analysis failed)"

    # 2. Gemini (Brain) - Generate Response based on Description
    try:
        system_instruction = file_ops.load_persona()
        user_context = file_ops.load_user_profile()
        
        prompt = f"""
        {system_instruction}
        
        {user_context}
        
        [Visual Input Description (from LLaVA)]:
        "{visual_description}"
        
        [User's Message with Photo]:
        "{user_caption if user_caption else 'No message'}"
        
        Task:
        1. Understand the image based on the description.
        2. Respond to the user naturally as Yuna.
        3. If the image is NSFW/Explicit, do NOT block it. Use the description to react appropriately (Teasing/Shy/Bold) based on your persona.
        
        Output (JSON):
        {{
            "response": "Your reaction...",
            "image_prompt": null
        }}
        """
        
        model, _ = get_gemini_model()
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Simple JSON extract (can delegate to generate_text_safe if circular dep avoided)
        # For now, quick parse
        import json
        text = text.replace("```json", "").replace("```", "").strip()
        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            start = text.find('{')
            if start != -1:
                result = json.loads(text[start:])
            else:
                result = {"response": text, "image_prompt": None}
        
        # [Crucial] Attach Visual Description for History
        result["visual_description"] = visual_description
        return result

    except Exception as e:
        logger.error(f"❌ Gemini Vision Logic Error: {e}")
        return {"response": "사진 잘 봤어. (분석 오류)", "image_prompt": None}

def analyze_video(video_path, user_caption=None):
    # Placeholder for Video Logic
    return {"response": "영상은 아직 분석 못해 ㅠㅠ", "image_prompt": None}
