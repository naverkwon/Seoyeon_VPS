
import random
from datetime import datetime
from .prompt_generator import (
    MALE_CHARACTER_PROFILES,
    MALE_MASTURBATION_ACTIONS,
    MALE_EXPRESSIONS,
    DUO_SCENARIOS,
    DUO_INTERACTION_DETAILS,
    CAMERA_ANGLES,
    CAMERA_LENS
)

# ==========================================
# Data Definitions & Constants
# ==========================================

# Placeholder dictionaries for variable content
POSES = {
    "default": ["standing", "sitting", "leaning against wall", "looking back"]
}
LOCATIONS = {
    "default": ["bedroom", "living room", "cafe", "street", "park", "studio"]
}
LIGHTING = {
    "default": ["soft lighting", "natural light", "cinematic lighting", "sunset light"]
}
EXPRESSIONS = {
    "default": ["smile", "seductive smile", "neutral", "looking at viewer"]
}
MALE_INTERACTIONS = {
    "default": ["hugging from behind", "holding hands", "leaning on shoulder"]
}
FANTASY_RACES = {
    "elf": {"features": "pointed ears", "hands": "elegant hands"},
    "werewolf": {"features": "wolf ears", "hands": "clawed hands"},
    "vampire": {"features": "pale skin, red eyes", "hands": "pale hands"}
}
NEGATIVE_PROMPTS = {
    "sfw": "nsfw, nude, naked, nipples, vaginal, anal, text, watermark, bad anatomy, bad hands, missing fingers",
    "tease": "nude, naked, nipples, vaginal, anal, text, watermark, bad anatomy, bad hands",
    "nsfw_moderate": "text, watermark, bad anatomy, bad hands",
    "nsfw_extreme": "text, watermark, bad anatomy, bad hands"
}

import json
import os

# Persistence
PROFILES_PATH = os.path.join(os.path.dirname(__file__), 'profiles.json')

def load_profiles():
    if os.path.exists(PROFILES_PATH):
        try:
            with open(PROFILES_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading profiles: {e}")
            return {}
    return {}

def save_profiles(profiles):
    try:
        with open(PROFILES_PATH, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving profiles: {e}")
        return False

# Load on module init
CHARACTER_PROFILES = load_profiles()

def refresh_profiles():
    """Reload profiles from disk and update the global dictionary in-place."""
    new_data = load_profiles()
    CHARACTER_PROFILES.clear()
    CHARACTER_PROFILES.update(new_data)
    return CHARACTER_PROFILES


# ==========================================
# Core Classes
# ==========================================

class CharacterProfile:
    def __init__(self, character_id, name, base_attributes, variable_attributes, constraints):
        self.character_id = character_id 
        self.name = name
        self.base_attributes = base_attributes  
        self.variable_attributes = variable_attributes 
        self.constraints = constraints 
        self.transformation_enabled = True # Default to True for now
        self.allowed_transformations = [] # List of allowed, empty means all if enabled 

class PromptTemplateBuilder:
    """
    Builds customized prompt templates for each character.
    """
    
    def __init__(self, character_profile):
        self.profile = character_profile
        self.base_template = self._build_base_template()
    
    def _build_base_template(self):
        """
        Constructs base template with character's fixed attributes.
        """
        quality = self.profile['quality_preset']
        fixed = self.profile['fixed_base']
        
        template = f"(masterpiece:{quality['masterpiece']}), (best quality:{quality['best_quality']}), {quality['detail_level']}, {quality['photo_type']}, {quality['render_style']}, sharp focus, extremely detailed face, realistic skin texture, pore details, professional studio lighting, beautiful young {fixed['ethnicity']} woman, {fixed['face_type']}, {fixed['age_range']}, {fixed['skin_tone']}, {fixed['facial_features']}, {fixed['makeup_style']}, {{HAIR_FULL}}, {fixed['bangs']}, {fixed['forehead']}, {fixed['body_type']}, {{BREAST_DESCRIPTION}}, {{CLOTHING_STATE}}, {{VARIABLE_CONTENT}}, depth of field"
        
        return template
    
    def build_hair_description(self, texture=None, state=None):
        """
        Dynamically generates hair description.
        """
        fixed = self.profile['fixed_base']
        variable = self.profile['variable_attributes']
        
        # Random choice if texture not specified
        if texture is None:
            texture = random.choice(variable['hair_texture'])
        
        # Random choice if state not specified
        if state is None:
            state = random.choice(variable['hair_state'])
        
        return f"{fixed['hair_length']} {texture} {fixed['hair_color']} hair {state}"
    
    def build_breast_description(self, size_level, clothing_level):
        """
        Generates breast description based on level and size.
        """
        size_options = self.profile['variable_attributes']['breast_size_options']
        
        # Size mapping
        size_map = {
            "small": "small to medium soft breasts with natural shape",
            "medium": "medium soft breasts with realistic slight sag",
            "medium-large": "medium-large soft breasts with realistic slight sag, soft pendulous breasts",
            "large": "large soft breasts with realistic sag, soft pendulous breasts",
            "extra-large": "extra-large soft breasts with realistic heavy sag, soft pendulous breasts"
        }
        
        # Check if selected size appears in character options
        if size_level not in size_options:
            size_level = size_options[-1]  # Fallback to largest option
        
        base_description = size_map[size_level]
        
        # Add description based on clothing level context (simplified logic here)
        return f"natural {base_description}"
    
    def validate_against_constraints(self, prompt_params):
        """
        Checks if the prompt violates character constraints.
        """
        constraints = self.profile['constraints']
        violations = []
        
        # Check prohibited hair styles
        if 'hair' in prompt_params:
            for prohibited in constraints['prohibited_hair']:
                if prohibited in prompt_params['hair'].lower():
                    violations.append(f"Prohibited hair style: {prohibited}")
        
        # Check prohibited features
        if 'features' in prompt_params:
            for prohibited in constraints['prohibited_features']:
                if prohibited in prompt_params['features'].lower():
                    violations.append(f"Prohibited feature: {prohibited}")
        
        # Style constraint check (e.g. Yuna - elegant only)
        if 'style_constraint' in constraints:
            if constraints['style_constraint'] == 'elegant_only':
                if 'category' in prompt_params and prompt_params['category'] in ['casual', 'sporty']:
                    violations.append(f"This character only supports elegant concepts")
        
        return len(violations) == 0, violations

class MultiCharacterPromptGenerator:
    """
    Manages multiple characters and generates prompts for them.
    """
    
    def __init__(self):
        self.characters = {}
        self.template_builders = {}
        
        # Load all character profiles
        for char_id, profile in CHARACTER_PROFILES.items():
            self.characters[char_id] = profile
            self.template_builders[char_id] = PromptTemplateBuilder(profile)
            
        # Male and Duo Data
        self.male_characters = MALE_CHARACTER_PROFILES
        self.male_masturbation = MALE_MASTURBATION_ACTIONS
        self.male_expressions = MALE_EXPRESSIONS
        self.duo_scenarios = DUO_SCENARIOS
        self.duo_interactions = DUO_INTERACTION_DETAILS
        self.camera_angles = CAMERA_ANGLES
        self.camera_lenses = CAMERA_LENS
    
    def list_characters(self):
        """List available characters"""
        return {char_id: profile['name'] for char_id, profile in self.characters.items()}
    
    def get_character_info(self, character_id):
        """Detailed info for specific character"""
        if character_id not in self.characters:
            raise ValueError(f"Character {character_id} not found")
        return self.characters[character_id]
    
    def generate_male_solo_prompt(self, male_character_id, hand_config, position, location, **kwargs):
        """
        Generate male solo masturbation prompt.
        """
        if male_character_id not in self.male_characters:
            raise ValueError(f"Male character {male_character_id} not found")
            
        male_profile = self.male_characters[male_character_id]
        action_data = self.male_masturbation['hand_positions'][hand_config]
        position_data = self.male_masturbation['body_positions'][position]
        
        # Speed
        speed = kwargs.get('speed', random.choice(action_data.get('speeds', ['fast'])))
        
        # Primary Action
        primary_action = action_data.get('primary_hand', action_data.get('action', '')).format(SPEED=speed)
        
        # Secondary Action
        secondary_hand = random.choice(action_data.get('secondary_hand', ['free']))
        
        # Motion Blur
        motion_blur = self.male_masturbation['motion_emphasis']['motion_blur_on_hand']
        
        # Expressions
        eye_expression = random.choice(self.male_expressions['intense_pleasure'])
        mouth_expression = random.choice(self.male_expressions['mouth'])
        
        # Body Position
        body_position = position_data.get('description', position)
        position_variation = random.choice(position_data.get('variations', ['']) or [''])
        
        variable_content = f"{body_position} {position_variation}, {primary_action} {motion_blur}, {secondary_hand}, {eye_expression}, {mouth_expression}, {location}"
        
        return self._build_male_prompt(male_character_id, variable_content, **kwargs)
    
    def generate_duo_prompt(self, female_character_id, male_character_id, position, location, **kwargs):
        """
        Generate duo (couple) prompt.
        """
        female_profile = self.characters.get(female_character_id)
        if not female_profile:
             raise ValueError(f"Female character {female_character_id} not found")
             
        male_profile = self.male_characters.get(male_character_id)
        if not male_profile:
             raise ValueError(f"Male character {male_character_id} not found")
        
        position_data = self.duo_scenarios['positions'][position]
        
        # Position Details
        male_position = position_data['male_position']
        female_position = position_data['female_position']
        
        # Hands
        male_hands = kwargs.get('male_hands', random.choice(position_data['male_hands']))
        female_hands = kwargs.get('female_hands', random.choice(position_data['female_hands']))
        
        # Physics & Interaction
        breast_physics = position_data.get('breast_physics', '')
        interaction = random.choice(self.duo_interactions['mutual_actions']['sounds'])
        
        # Location / Furniture
        if '{FURNITURE}' in position_data.get('description', ''):
            furniture = random.choice(position_data.get('furniture_options', ['desk']))
            description = position_data['description'].format(FURNITURE=furniture)
        else:
            description = position_data['description'].format(LOCATION=location)
        
        variable_content = f"{description}, {male_position}, {female_position}, {breast_physics}, {male_hands}, {female_hands}, {interaction}"
        
        return self._build_duo_prompt(female_profile, male_profile, variable_content, **kwargs)
    
    def _build_male_prompt(self, male_character_id, variable_content, **kwargs):
        """Helper to build full male prompt string"""
        profile = self.male_characters[male_character_id]
        fixed = profile['fixed_base']
        
        # Camera Logic
        cam_angle = kwargs.get('camera_angle') or random.choice(self.camera_angles)
        cam_lens = kwargs.get('camera_lens') or random.choice(self.camera_lenses)

        template = f"(masterpiece:{profile['quality_preset']['masterpiece']}), (best quality:{profile['quality_preset']['best_quality']}), {profile['quality_preset']['detail_level']}, {profile['quality_preset']['photo_type']}, {profile['quality_preset']['render_style']}, sharp focus, extremely detailed face, realistic skin texture, pore details, professional studio lighting, {cam_angle}, {cam_lens}, handsome young {fixed['ethnicity']} man {profile['name']}, {fixed['face_type']}, {fixed['hair_style']}, {fixed['age_range']}, {fixed['skin_tone']}, {fixed['body_type']}, {fixed['body_details']}, realistic medium-large erect penis with visible veins, {variable_content}, depth of field"
        
        return {
            'positive': template,
            'negative': "unrealistically large penis, giant penis, deformed penis, female, childlike, low quality, blurry, watermark",
            'metadata': {
                'character_id': male_character_id,
                'character_name': profile['name'],
                'gender': 'male',
                'type': 'solo'
            }
        }
    
    def _build_duo_prompt(self, female_profile, male_profile, variable_content, **kwargs):
        """Helper to build full duo prompt string"""
        f_fixed = female_profile['fixed_base']
        m_fixed = male_profile['fixed_base']
        
        # Descriptions
        female_desc = f"beautiful young {f_fixed['ethnicity']} woman {female_profile['name']} with long damp straight black hair no bangs"
        male_desc = f"handsome {m_fixed['ethnicity']} man {male_profile['name']} with {m_fixed['hair_style']}"
        
        # Bodies
        # Note: Using hardcoded breast desc for now as per user snippet example logic, or dynamic if preferred. 
        # Using snippet logical base.
        female_body = f"{female_profile['name']} slim body natural extra-large soft breasts with heavy sag completely nude"
        male_body = f"{male_profile['name']} {m_fixed['body_type']} realistic medium-large erect penis"
        
        # Camera Logic
        cam_angle = kwargs.get('camera_angle') or random.choice(self.camera_angles)
        cam_lens = kwargs.get('camera_lens') or random.choice(self.camera_lenses)
        
        template = f"(masterpiece:1.3), (best quality:1.3), ultra detailed, 8k RAW photo, photorealistic, sharp focus, extremely detailed face, realistic skin texture, pore details, professional studio lighting, {cam_angle}, {cam_lens}, {female_desc} and {male_desc}, both early 20s, {female_body}, {male_body}, {variable_content}, depth of field"
        
        return {
            'positive': template,
            'negative': "childlike, low quality, blurry, deformed, watermark, text, extra limbs, clothing, bad anatomy",
            'metadata': {
                'female_character': female_profile['name'],
                'male_character': male_profile['name'],
                'type': 'duo'
            }
        }

    def generate_prompt(self, character_id, level, category, **kwargs):
        """
        Generate prompt for specific character.
        
        Args:
            character_id: "seoyeon", "minjee", "yuna" etc.
            level: "sfw", "tease", "nsfw_moderate", "nsfw_extreme"
            category: "general", "with_male", "fantasy" etc.
            **kwargs: additional customizing options
        """
        if character_id not in self.characters:
            raise ValueError(f"Character {character_id} not found")
        
        builder = self.template_builders[character_id]
        profile = self.characters[character_id]
        
        # 1. Hair Settings
        hair_texture = kwargs.get('hair_texture', None)
        hair_state = kwargs.get('hair_state', None)
        hair_full = builder.build_hair_description(hair_texture, hair_state)
        
        # 2. Breast Size Settings
        breast_size = kwargs.get('breast_size', profile['variable_attributes']['breast_size_options'][-1])
        breast_description = builder.build_breast_description(breast_size, level)
        
        # 3. Clothing State
        clothing_state = self._get_clothing_state(level, category)
        
        # 4. Variable Content (Poses, Expressions, Background, Lighting)
        variable_content = self._build_variable_content(level, category, **kwargs)
        
        # 5. Template Combination
        base_template = builder.base_template
        
        prompt_params = {
            'hair': hair_full,
            'features': profile['fixed_base']['facial_features'],
            'category': category
        }
        
        # 6. Constraint Validation
        is_valid, violations = builder.validate_against_constraints(prompt_params)
        if not is_valid:
            raise ValueError(f"Constraint violations: {violations}")
        
        # 7. Final Prompt Generation
        final_prompt = base_template.format(
            HAIR_FULL=hair_full,
            BREAST_DESCRIPTION=breast_description,
            CLOTHING_STATE=clothing_state,
            VARIABLE_CONTENT=variable_content
        )
        
        return {
            'positive': final_prompt,
            'negative': self._get_negative_prompt(level, character_id),
            'metadata': {
                'character_id': character_id,
                'character_name': profile['name'],
                'level': level,
                'category': category,
                'lora_trigger': profile['lora_trigger']
            }
        }
    
    def generate_batch(self, character_id, level, category, count=10, **kwargs):
        """
        Generate batch prompts for one character
        """
        prompts = []
        for i in range(count):
            try:
                prompt = self.generate_prompt(character_id, level, category, **kwargs)
                prompt['metadata']['batch_index'] = i + 1
                prompts.append(prompt)
            except ValueError as e:
                print(f"Skipped prompt {i+1}: {e}")
                continue
        
        return prompts
    
    def generate_multi_character_batch(self, character_ids, level, category, count_per_character=5, **kwargs):
        """
        Generate prompts for multiple characters simultaneously
        """
        all_prompts = {}
        
        for char_id in character_ids:
            all_prompts[char_id] = self.generate_batch(
                char_id, level, category, count_per_character, **kwargs
            )
        
        return all_prompts
    
    def _get_clothing_state(self, level, category):
        """Determine clothing state"""
        if level == "sfw":
            return "fully covered"
        elif level == "tease":
            return "wearing suggestive clothing"
        elif level == "nsfw_moderate":
            return "partially covered"
        elif level == "nsfw_extreme":
            return "topless" if category != "fantasy" else "topless"
        
        return "fully covered"
    
    def _build_variable_content(self, level, category, **kwargs):
        """Generate variable content"""
        
        pose = kwargs.get('pose', random.choice(POSES['default']))
        location = kwargs.get('location', random.choice(LOCATIONS['default']))
        lighting = kwargs.get('lighting', random.choice(LIGHTING['default']))
        expression = kwargs.get('expression', random.choice(EXPRESSIONS['default']))
        
        content = f"{pose}, {expression}, {location}, {lighting}"
        
        # Category specific additions
        if category == "with_male":
            content += f", {random.choice(MALE_INTERACTIONS['default'])}"
        elif category == "fantasy":
            race = kwargs.get('race', 'werewolf')
            if race in FANTASY_RACES:
                content += f", with {FANTASY_RACES[race]['features']}, {FANTASY_RACES[race]['hands']} touching"
        
        return content
    
    def _get_negative_prompt(self, level, character_id):
        """Character-specific negative prompt"""
        profile = self.characters[character_id]
        base_negative = NEGATIVE_PROMPTS.get(level, NEGATIVE_PROMPTS['sfw'])
        
        # Add character prohibited elements
        character_prohibitions = []
        for prohibited in profile['constraints']['prohibited_hair']:
            character_prohibitions.append(prohibited)
        for prohibited in profile['constraints']['prohibited_features']:
            character_prohibitions.append(prohibited)
        
        combined_negative = base_negative + ", " + ", ".join(character_prohibitions)
        
        return combined_negative

class CharacterComparator:
    """
    Analyzes and compares characters.
    """
    
    def __init__(self, generator):
        self.generator = generator
    
    def compare_characters(self, char_id_1, char_id_2):
        """Analyze differences between two characters"""
        char1 = self.generator.characters[char_id_1]
        char2 = self.generator.characters[char_id_2]
        
        differences = {
            'visual': {},
            'constraints': {},
            'capabilities': {}
        }
        
        # Fixed base comparison
        for key in char1['fixed_base']:
            if char1['fixed_base'][key] != char2['fixed_base'][key]:
                differences['visual'][key] = {
                    char_id_1: char1['fixed_base'][key],
                    char_id_2: char2['fixed_base'][key]
                }
        
        # Variable attributes comparison
        for key in char1['variable_attributes']:
            if key in char2['variable_attributes']:
                if set(char1['variable_attributes'][key]) != set(char2['variable_attributes'][key]):
                    differences['capabilities'][key] = {
                        char_id_1: char1['variable_attributes'][key],
                        char_id_2: char2['variable_attributes'][key]
                    }
        
        # Constraints comparison
        for key in char1['constraints']:
            if key in char2['constraints']:
                if char1['constraints'][key] != char2['constraints'][key]:
                    differences['constraints'][key] = {
                        char_id_1: char1['constraints'][key],
                        char_id_2: char2['constraints'][key]
                    }
        
        return differences
    
    def get_character_matrix(self):
        """Main feature matrix for all characters"""
        characters = self.generator.list_characters()
        
        matrix = []
        for char_id in characters:
            profile = self.generator.characters[char_id]
            matrix.append({
                'id': char_id,
                'name': profile['name'],
                'age': profile['fixed_base']['age_range'],
                'skin': profile['fixed_base']['skin_tone'],
                'face': profile['fixed_base']['face_type'],
                'bangs': profile['fixed_base']['bangs'],
                'body': profile['fixed_base']['body_type'],
                'breast_range': f"{profile['variable_attributes']['breast_size_options'][0]} ~ {profile['variable_attributes']['breast_size_options'][-1]}"
            })
        
        return matrix

class CharacterVersionManager:
    """
    Manages Character LoRA Versions
    """
    
    def __init__(self):
        self.versions = {}
    
    def create_new_version(self, base_character_id, version_number, changes):
        """
        Create new version of existing character
        
        Args:
            base_character_id: "seoyeon"
            version_number: "v2"
            changes: Dictionary of changes
        """
        base_profile = CHARACTER_PROFILES[base_character_id].copy()
        new_id = f"{base_character_id}_{version_number}"
        
        new_profile = base_profile.copy()
        new_profile['id'] = new_id
        new_profile['lora_trigger'] = f"{base_character_id}_{version_number}"
        
        # Apply changes
        for category, updates in changes.items():
            if category in new_profile:
                if isinstance(new_profile[category], dict):
                    new_profile[category].update(updates)
                else:
                    new_profile[category] = updates
        
        # Record version history
        if base_character_id not in self.versions:
            self.versions[base_character_id] = []
        
        self.versions[base_character_id].append({
            'version': version_number,
            'id': new_id,
            'changes': changes,
            'created_at': datetime.now()
        })
        
        CHARACTER_PROFILES[new_id] = new_profile
        
        return new_id
    
    def get_version_history(self, character_id):
        """Get version history for character"""
        return self.versions.get(character_id, [])

def add_new_character(character_data):
    """
    Add new character to the system
    
    Args:
        character_data: Character profile dictionary
    """
    # 1. Required field validation
    required_fields = ['id', 'name', 'lora_trigger', 'fixed_base', 'variable_attributes', 'constraints']
    for field in required_fields:
        if field not in character_data:
            raise ValueError(f"Missing required field: {field}")
    
    # 2. fixed_base validation
    required_fixed_base = ['ethnicity', 'face_type', 'age_range', 'skin_tone', 
                           'facial_features', 'makeup_style', 'hair_color', 
                           'hair_length', 'bangs', 'forehead', 'body_type', 'gender']
    for attr in required_fixed_base:
        if attr not in character_data['fixed_base']:
            raise ValueError(f"Missing fixed_base attribute: {attr}")
    
    # 3. Add to CHARACTER_PROFILES
    # FIX: Handle names with underscores (don't use split('_')[0])
    raw_id = character_data['id']
    if raw_id.endswith('_v1'):
        char_id = raw_id[:-3]
    else:
        char_id = raw_id
            
    CHARACTER_PROFILES[char_id] = character_data
    
    # Save to disk
    if save_profiles(CHARACTER_PROFILES):
        print(f"Character '{character_data['name']}' (ID: {char_id}) added and saved successfully!")
    else:
        print(f"Character added to memory but FAILED to save to disk.")
    
    return char_id

def delete_character(char_id):
    """
    Remove character from the system
    
    Args:
        char_id: Character ID to remove
    """
    if char_id in CHARACTER_PROFILES:
        name = CHARACTER_PROFILES[char_id]['name']
        del CHARACTER_PROFILES[char_id]
        
        if save_profiles(CHARACTER_PROFILES):
            print(f"Character '{name}' (ID: {char_id}) deleted successfully!")
            return True
        else:
            print(f"Failed to save changes after deleting {char_id}")
            return False
            
    return False
