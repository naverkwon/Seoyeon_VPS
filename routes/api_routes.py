
from flask import Blueprint, jsonify, request
import os
import random
import sys
from lora_system.lora_manager import MultiCharacterPromptGenerator, CHARACTER_PROFILES, add_new_character, refresh_profiles, delete_character
from lora_system.prompt_generator import PromptGenerator, MALE_CHARACTER_PROFILES
from services.image_gen import ImageGenerator
from lora_system.data.constants import HAIR_STYLES, LOCATIONS, POSES, TOPS, BOTTOMS, OUTERWEAR, FULL_BODY
from werkzeug.utils import secure_filename

api_bp = Blueprint('api', __name__)

# Initialize Generators (Lazy load or shared instance pattern would be better, but this works for now)
# Note: We need to ensure these are singletons or shared if state matters.
multi_char_gen = MultiCharacterPromptGenerator()
auto_prompt_gen = PromptGenerator()

@api_bp.route('/api/characters', methods=['GET'])
def get_characters():
    """Return available characters and valid profiles"""
    chars = []
    # Force reload
    refresh_profiles()
    
    # We need to access app config to check for files, but we are in a blueprint.
    # accessible via current_app
    from flask import current_app
    
    for char_id, profile in CHARACTER_PROFILES.items():
        # PRIORITIZE profile's base_image if set
        if 'base_image' in profile:
            img_path = profile['base_image']
        else:
             # Fallback to ID-based
             img_path = f"/static/images/{char_id}.jpg"
             # Check if file exists using current_app.config['UPLOAD_FOLDER'] 
             # (Assuming config is available, otherwise construct path)
             upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'static', 'images'))
             
             if not os.path.exists(os.path.join(upload_folder, f"{char_id}.jpg")):
                  img_path = "/static/images/placeholder.jpg"

        # Cache busting for local files
        if img_path.startswith("/static/"):
            try:
                local_f = os.path.join(os.getcwd(), img_path.lstrip('/'))
                if os.path.exists(local_f):
                     ts = int(os.path.getmtime(local_f))
                     img_path = f"{img_path}?v={ts}"
            except:
                pass
             
        chars.append({
            "id": char_id,
            "name": profile['name'],
            "description": profile.get('fixed_base', {}).get('face_type', 'Custom Character'),
            "base_image": img_path,
            "profile_data": profile # Return full data for editing
        })
    return jsonify({"success": True, "characters": chars})

@api_bp.route('/api/save-character', methods=['POST'])
def save_character():
    try:
        data = request.json
        char_id = data.get('id')
        name = data.get('name')
        
        # Basic validation
        if not char_id or not name:
            return jsonify({'success': False, 'error': 'Missing ID or Name'})

        # Construct profile object (Simplified for brevity, assuming full payload structure)
        # For a cleaner refactor, this logic could move to a Controller/Service layer.
        profile_data = {
            "lora_trigger": data.get('lora_trigger', ''),
            "fixed_base": {
                "ethnicity": data.get('ethnicity', 'Korean'),
                "gender": data.get('gender', 'female'),
                "face_type": data.get('face_type', ''),
                "facial_features": data.get('facial_features', ''),
                "age_range": data.get('age_range', 'early 20s'),
                "hair_color": data.get('hair_color', ''),
                "hair_length": data.get('hair_length', ''),
                "body_type": data.get('body_type', '')
            },
            "variable_attributes": {}, # Defaults
            "constraints": {},
            "quality_preset": "masterpiece"
        }

        add_new_character(char_id, name, profile_data)
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/api/delete-character', methods=['POST'])
def remove_character():
    data = request.json
    char_id = data.get('id')
    if delete_character(char_id):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Character not found'})

@api_bp.route('/api/generate-prompt', methods=['POST'])
def generate_prompt_api():
    data = request.json
    mode = data.get('mode', 'auto')
    char_id = data.get('character_id', 'seoyeon')
    count = int(data.get('count', 1))
    
    # 1. Check builder override
    if mode == 'builder':
        # Allow level override, don't force 'builder' string which defaults to SFW
        level = data.get('level', 'sfw')
        # Extract builder overrides
        manual_override = {
            'hair': data.get('hair'),
            'outfit': {
                'top': data.get('top'),
                'bottom': data.get('bottom'),
                'outer': data.get('outer')
            } if any([data.get('top'), data.get('bottom'), data.get('outer')]) else None,
            'pose': data.get('pose'),
            'location': data.get('location'),
            'camera_angle': data.get('camera_angle'),
            'camera_lens': data.get('camera_lens')
        }
        # Clean None values
        if manual_override['outfit']:
            manual_override['outfit'] = {k: v for k, v in manual_override['outfit'].items() if v}
        manual_override = {k: v for k, v in manual_override.items() if v}

    else:
        level = data.get('level', 'sfw') # sfw, tease, nsfw
        manual_override = None

    category = data.get('category', 'general') # general, self_photo, fantasy, etc.

    # 2. Get Profile
    profile = CHARACTER_PROFILES.get(char_id, CHARACTER_PROFILES['seoyeon'])
    
    prompts = []
    
    # 3. Generate
    if category == 'duo' and data.get('duo_partner'):
        # Duo Logic (Simplified for API migration)
        pass 
        
    elif data.get('male_character') and category == 'with_male':
         # Male Interaction Logic
        male_id = data.get('male_character')
        
        # [FIX] Handle Random Male selection if ID is empty/random
        if not male_id or male_id == "random":
             male_id = random.choice(list(MALE_CHARACTER_PROFILES.keys()))

        male_profile = MALE_CHARACTER_PROFILES.get(male_id)
        
        # Use MultiCharacter Generator
        for _ in range(count):
             # Force position or random
            pos = data.get('duo_position') or random.choice(['male_behind', 'male_front', 'side_by_side'])
            prompts.append(
                multi_char_gen.generate_duo_prompt(profile, male_profile, pos, level)
            )

    else:
        # Standard Solo Generation (can use batch generate directly)
        batch_results = auto_prompt_gen.generate(level, category, count, manual_override, profile)
        
        # Post-Processing for Frontend (Summary & Name)
        from lora_system.data.constants import K_TRANS
        
        for p in batch_results:
            meta = p['metadata'].get('components', {})
            loc = meta.get('location', '')
            pose = meta.get('pose', '')
            
            # Simple Translation
            k_loc = K_TRANS.get(loc, loc)
            k_pose = K_TRANS.get(pose, pose)
            
            # Fetch Character Name
            char_name_display = profile.get('name', char_id) if profile else char_id
            
            # Summary
            p['korean_summary'] = f"[{char_name_display}] 📍 {k_loc}에서 {k_pose}"
            
        prompts.extend(batch_results)

    return jsonify({'success': True, 'prompts': prompts})

@api_bp.route('/api/generate-image', methods=['POST'])
def generate_image_api():
    data = request.json
    prompt = data.get('prompt')
    seed = data.get('seed') # Optional
    
    if not prompt:
        return jsonify({'success': False, 'error': 'No prompt provided'})

    local_path, url, used_seed = ImageGenerator.generate(prompt, seed=seed)
    
    if local_path:
        return jsonify({
            'success': True, 
            'local_path': local_path, 
            'url': url,
            'seed': used_seed
        })
    else:
        return jsonify({'success': False, 'error': 'Generation failed'})

@api_bp.route('/api/gallery', methods=['GET'])
def get_gallery():
    # Helper to list images
    generated_dir = os.path.join(os.getcwd(), 'generated_images')
    if not os.path.exists(generated_dir):
        return jsonify([])
        
    images = []
    for f in sorted(os.listdir(generated_dir), reverse=True):
        if f.endswith(('.png', '.jpg', '.jpeg')):
            images.append(f)
            
    return jsonify(images[:50]) # Limit to 50
