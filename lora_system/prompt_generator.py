import random
from .data.constants import (
    HAIR_STYLES, BREAST_SIZES, CLOTHING_STATES, TOPS, BOTTOMS, OUTERWEAR,
    FULL_BODY, POSES, LOCATIONS, LIGHTING, EXPRESSIONS, CAMERA_ANGLES,
    CAMERA_LENS, MALE_INTERACTIONS, FANTASY_RACES, NEGATIVE_PROMPTS,
    HASHTAGS, CAPTIONS, RACE_TRANSFORMATIONS, MASTURBATION_ACTIONS,
    CLOTHING_EXPOSURE_STATES, PUBLIC_LOCATIONS, PUBLIC_EXPRESSIONS
)

# ==========================================
# Data Constants
# ==========================================

FIXED_BASE = "(masterpiece:1.3), (best quality:1.3), ultra detailed, 8k RAW photo, photorealistic, sharp focus, extremely detailed face, realistic skin texture, pore details, professional studio lighting, {CAMERA_ANGLE}, {CAMERA_LENS}, beautiful young Korean woman, Korean idol face, early 20s, fair skin, delicate sharp features, huge clear eyes, natural minimal makeup, {HAIR_VARIATION}, no bangs, forehead fully exposed, slim body, {BREAST_SIZE}, {CLOTHING_STATE}, {VARIABLE_CONTENT}, depth of field"

# Helper to combine parts
def _generate_outfit_string(overrides=None):
    overrides = overrides or {}
    
    # Priority: Direct overrides -> Random Combination
    if overrides.get('top') or overrides.get('bottom') or overrides.get('outer'):
        parts = []
        if overrides.get('top'): parts.append(overrides['top'])
        if overrides.get('bottom'): parts.append(overrides['bottom'])
        if overrides.get('outer'): parts.append(overrides['outer'])
        return ", ".join(parts)
        
    # Random Logic
    # 30% chance of Full Body, 70% chance of Top+Bottom
    if random.random() < 0.3:
        base = random.choice(FULL_BODY)
        if random.random() < 0.4: # 40% chance of Outer
            return f"{base} with {random.choice(OUTERWEAR)}"
        return base
    else:
        top = random.choice(TOPS)
        bottom = random.choice(BOTTOMS)
        outfit = f"{top} paired with {bottom}"
        if random.random() < 0.4: # 40% chance of Outer
            outfit += f", wearing {random.choice(OUTERWEAR)}"
        return outfit


VALIDATION_RULES = {
    "must_have": [
        "no bangs",
        "forehead fully exposed",
        "depth of field",
        "Korean woman"
    ],
    "must_not_have_sfw": [
        "topless", "nipple", "areola", "naked"
    ],
    "max_length": 1500,
    "min_length": 200
}





# ==========================================
# New Male & Duo Categories (User Provided)
# ==========================================

MALE_CHARACTER_PROFILES = {
    "jun": {
        "id": "jun_v1",
        "name": "Jun",
        "gender": "male",
        "lora_trigger": "jun",
        "fixed_base": {
            "ethnicity": "Korean",
            "face_type": "sharp jawline, intense dark eyes",
            "age_range": "early 20s",
            "skin_tone": "fair skin",
            "facial_features": "sharp jawline, intense dark eyes",
            "hair_style": "short black undercut hair",
            "body_type": "tall muscular athletic body",
            "body_details": "defined abs"
        },
        "variable_attributes": {
            "hair_state": ["neat", "messy", "damp with sweat"],
            "penis_size_options": ["medium-large realistic"],
            "body_state": ["athletic", "muscular", "toned"]
        },
        "constraints": {
            "prohibited_features": ["childlike", "unrealistically large penis", "giant penis", "deformed penis"],
            "age_constraint": "must_be_adult",
            "realistic_anatomy": True
        },
        "quality_preset": {
            "masterpiece": 1.3,
            "best_quality": 1.3,
            "detail_level": "ultra detailed",
            "photo_type": "8k RAW photo",
            "render_style": "photorealistic"
        }
    }
}

MALE_MASTURBATION_ACTIONS = {
    "hand_positions": {
        "one_hand_stroking": {
            "primary_hand": "hand gripping shaft tightly stroking {SPEED}",
            "secondary_hand": ["free", "on balls", "teasing nipple", "on abs", "gripping sheet"],
            "speeds": ["slowly", "fast", "rapidly"]
        },
        "both_hands_stroking": {
            "action": "both hands on shaft stroking {SPEED}",
            "variations": ["alternating", "together", "one on shaft one on tip"],
            "speeds": ["slowly", "fast", "edging"]
        },
        "edging": {
            "action": "slow edging stroke with visible hand grip",
            "secondary": ["teasing tip", "squeezing balls", "stopping before climax"],
            "focus": "control and prolonged pleasure"
        }
    },
    "motion_emphasis": {
        "motion_blur_on_hand": "with motion blur on hand",
        "visible_grip": "with visible hand grip",
        "speed_indicators": ["stroking fast", "stroking slowly", "pumping", "edging"]
    },
    "body_positions": {
        "lying_on_back": {
            "variations": ["legs bent", "legs flat", "hips raised"],
            "hand_access": "easy two-hand access"
        },
        "sitting": {
            "variations": [
                "on bed edge",
                "on chair backwards",
                "on sofa",
                "on desk chair"
            ],
            "posture": ["leaning back", "upright", "head thrown back"]
        },
        "standing": {
            "variations": [
                "in front of mirror",
                "in shower",
                "against wall",
                "by window"
            ],
            "support": ["one hand on wall", "both hands free", "leaning forward"]
        },
        "on_stomach": {
            "variations": ["flat", "ass up", "hips raised"],
            "action": "hand under body stroking"
        },
        "kneeling": {
            "variations": ["upright", "on bed", "facing mirror"],
            "action": "stroking while kneeling"
        }
    }
}

MALE_EXPRESSIONS = {
    "intense_pleasure": [
        "eyes narrowed in pleasure",
        "eyes half-closed",
        "eyes rolled back slightly",
        "intense eye contact",
        "eyes locked on viewer"
    ],
    "mouth": [
        "biting lip",
        "biting lower lip hard",
        "gritted teeth",
        "moaning open mouth",
        "heavy breathing expression"
    ],
    "facial_tension": [
        "jaw clenched",
        "jawline clenched",
        "furrowed brow",
        "furrowed brow pleasure face"
    ],
    "concentration": [
        "eyes narrowed in concentration",
        "staring intensely",
        "watching himself with pleasure expression"
    ]
}

DUO_SCENARIOS = {
    "positions": {
        "missionary": {
            "male_position": "on top inserting deeply",
            "female_position": "legs wrapped around his waist",
            "male_hands": ["gripping her hips", "on bed supporting", "squeezing breasts"],
            "female_hands": ["squeezing own breasts", "on his back", "gripping sheets"],
            "description": "missionary on {LOCATION}"
        },
        "doggy_style": {
            "male_position": "behind inserting from behind",
            "female_position": "on all fours",
            "male_hands": ["gripping hips", "reaching under stroking clit", "pulling hair gently", "spanking"],
            "female_hands": ["on bed supporting", "reaching back", "squeezing own breast"],
            "breast_physics": "heavy breasts hanging and swinging",
            "description": "doggy style on {LOCATION}"
        },
        "cowgirl": {
            "male_position": "lying on back",
            "female_position": "riding on top",
            "variations": ["facing him", "reverse cowgirl"],
            "male_hands": ["on her hips", "squeezing breasts", "on her thighs"],
            "female_hands": ["on his chest", "on his thighs behind", "squeezing own breasts"],
            "breast_physics": "heavy breasts bouncing",
            "description": "cowgirl on {LOCATION}"
        },
        "standing": {
            "male_position": "lifting her",
            "female_position": "legs wrapped around him",
            "male_hands": ["supporting under thighs", "on hips"],
            "female_hands": ["around his neck", "gripping shoulders"],
            "breast_contact": "breasts pressed against his chest",
            "description": "standing against {LOCATION}"
        },
        "spooning": {
            "male_position": "behind inserting",
            "female_position": "lying on side, leg lifted",
            "male_hands": ["squeezing breast", "rubbing clit", "on hip"],
            "female_hands": ["reaching back touching him", "on own breast"],
            "intimacy": "close intimate position",
            "description": "spooning on {LOCATION}"
        },
        "69": {
            "male_position": "lying on back",
            "female_position": "on top facing opposite",
            "male_action": "tongue on her pussy",
            "female_action": "mouth on his penis",
            "breast_contact": "heavy breasts pressed on his abs",
            "description": "69 position on {LOCATION}"
        },
        "prone_bone": {
            "male_position": "on top inserting",
            "female_position": "lying flat on stomach",
            "male_hands": ["reaching under squeezing breast", "on her back", "gripping pillow"],
            "female_position_detail": "breasts squished under her, face in pillow",
            "description": "prone bone on {LOCATION}"
        },
        "lotus": {
            "male_position": "sitting cross-legged",
            "female_position": "in his lap facing him inserting",
            "male_hands": ["lifting breasts", "on her back", "supporting"],
            "female_hands": ["on his shoulders", "around his neck"],
            "intimacy": "deep eye contact, very intimate",
            "description": "lotus position on {LOCATION}"
        },
        "bent_over": {
            "male_position": "standing inserting from behind",
            "female_position": "bent over {FURNITURE}",
            "male_hands": ["on hips", "pulling hair gently", "reaching under"],
            "female_position_detail": "breasts resting on {FURNITURE}",
            "furniture_options": ["desk", "counter", "railing", "table"],
            "description": "bent over {FURNITURE}"
        },
        "piledriver": {
            "male_position": "inserting from above",
            "female_position": "legs over head",
            "male_hands": ["on her thighs", "supporting legs"],
            "female_position_detail": "heavy breasts hanging toward face",
            "intensity": "very intense angle",
            "description": "piledriver on {LOCATION}"
        }
    },
    
    "duo_locations": {
        "bedroom": ["hotel bed", "bed", "mattress"],
        "bathroom": ["shower", "bathtub", "jacuzzi", "sauna"],
        "furniture": ["sofa", "desk", "chair", "counter", "piano"],
        "windows": ["floor-to-ceiling window", "balcony railing", "glass wall"],
        "unique": ["elevator", "rooftop daybed", "minibar counter", "pool edge"]
    }
}

DUO_INTERACTION_DETAILS = {
    "mutual_actions": {
        "kissing": [
            "kissing passionately",
            "deep kiss",
            "neck kissing",
            "biting neck gently"
        ],
        "eye_contact": [
            "intense eye contact",
            "deep eye contact",
            "both looking at each other",
            "her looking back at him"
        ],
        "sounds": [
            "both moaning",
            "mutual pleasure expressions",
            "her gasping, him grunting",
            "both ecstatic expressions"
        ]
    },
    
    "breast_interaction": {
        "male_touching": [
            "his hands squeezing breasts",
            "reaching around squeezing breast",
            "reaching under squeezing breast",
            "lifting heavy breasts",
            "pinching nipples"
        ],
        "female_self": [
            "her hands squeezing own breasts",
            "one hand squeezing own breast"
        ],
        "physics": [
            "breasts bouncing",
            "breasts swinging",
            "breasts pressed against {BODY_PART}",
            "breasts squished on {SURFACE}",
            "breasts hanging"
        ]
    },
    
    "additional_stimulation": {
        "female": [
            "his hand rubbing her clit",
            "reaching under stroking clit",
            "fingers on clit while inserting"
        ],
        "male": [
            "her hand on his balls",
            "squeezing his ass",
            "scratching his back"
        ]
    }
}


class PromptGenerator:
    def __init__(self):
        # Default base if no profile provided
        self.base = FIXED_BASE
        self.negative = NEGATIVE_PROMPTS
        
        # New Advanced Data
        self.transformations = RACE_TRANSFORMATIONS
        self.masturbation_actions = MASTURBATION_ACTIONS
        self.clothing_exposures = CLOTHING_EXPOSURE_STATES
        self.public_locations = PUBLIC_LOCATIONS
        
        # Camera Details
        self.camera_angles = CAMERA_ANGLES
        self.camera_lenses = CAMERA_LENS
        
    def _build_base_string(self, profile):
        """Construct prompt base dynamically from character profile"""
        if not profile or 'fixed_base' not in profile:
            # Inject trigger if known but no full profile
            if profile and 'lora_trigger' in profile:
                 return self.base.replace("Korean idol face,", f"Korean idol face, {profile['lora_trigger']},")
            return self.base
            
        fixed = profile['fixed_base']
        # Construct template using profile fields
        # Note: We map profile keys to the expected format
        trigger = profile.get('lora_trigger', '')
        
        # Build the string
        # e.g. "..., beautiful young {ethnicity} woman, {face_type}, {trigger}, {age_range}, ..."
        base = f"(masterpiece:1.3), (best quality:1.3), ultra detailed, 8k RAW photo, photorealistic, sharp focus, extremely detailed face, realistic skin texture, pore details, professional studio lighting, {{CAMERA_ANGLE}}, {{CAMERA_LENS}}, beautiful young {fixed.get('ethnicity', 'Korean')} woman, {fixed.get('face_type', 'Korean idol face')}, {trigger}, {fixed.get('age_range', 'early 20s')}, {fixed.get('skin_tone', 'fair skin')}, {fixed.get('facial_features', '')}, {fixed.get('makeup_style', 'natural makeup')}, {{HAIR_VARIATION}}, {fixed.get('bangs', 'no bangs')}, {fixed.get('forehead', 'forehead visible')}, {fixed.get('body_type', 'slim body')}, {{BREAST_SIZE}}, {{CLOTHING_STATE}}, {{VARIABLE_CONTENT}}, depth of field"
        
        # Clean up any empty segments (e.g. if facial_features is empty)
        base = base.replace(", ,", ",")
        return base
    
    def generate(self, level="sfw", category="general", count=10, manual_override=None, character_profile=None, **kwargs):
        """
        manual_override: dict with keys 'hair', 'outfit', 'pose', 'location'
        """
        prompts = []
        
        for i in range(count):
            if level == "sfw":
                prompt, p_meta = self._generate_sfw(category, manual_override=manual_override, profile=character_profile, **kwargs)
            elif level == "tease":
                prompt, p_meta = self._generate_tease(category, manual_override=manual_override, profile=character_profile, **kwargs)
            elif level == "nsfw_moderate":
                prompt, p_meta = self._generate_nsfw_moderate(category, manual_override=manual_override, profile=character_profile, **kwargs)
            elif level == "nsfw_extreme":
                prompt, p_meta = self._generate_nsfw_extreme(category, manual_override=manual_override, profile=character_profile, **kwargs)
            else:
                prompt, p_meta = self._generate_sfw(category, manual_override=manual_override, profile=character_profile, **kwargs) 
            
            # Determine negative prompt key
            neg_key = level
            if level in ["nsfw_moderate", "nsfw_extreme"]:
                neg_key = "nsfw"
            if category == "fantasy":
                neg_key = "fantasy"
            
            prompts.append({
                'positive': prompt,
                'negative': self.negative.get(neg_key, self.negative['sfw']),
                'metadata': {
                    'level': level,
                    'category': category,
                    'index': i+1,
                    'components': p_meta 
                }
            })
        
        return prompts
    
    def _generate_sfw(self, category, manual_override=None, profile=None, **kwargs):
        manual_override = manual_override or {}
        
        # Determine base template
        base_template = self._build_base_string(profile)
        
        hair = manual_override.get('hair') or random.choice(HAIR_STYLES)
        breast = BREAST_SIZES["sfw_small"]
        
        
        # Select outfit using new logic or overrides
        outfit = _generate_outfit_string(manual_override)
        if manual_override.get('outfit'): # Support legacy 'outfit' key
             outfit = manual_override['outfit']
        
        # Location logic
        location = manual_override.get('location')
        if not location:
            location = random.choice(LOCATIONS['indoor_cozy'])
            if category == 'transport':
                location = random.choice(LOCATIONS['transport'])
            
        pose = manual_override.get('pose') or random.choice(POSES['sitting'] + POSES['standing'])
        expression = random.choice(EXPRESSIONS['soft'])
        lighting = random.choice(LIGHTING['natural'])
        
        variable_content = f"wearing {outfit}, {pose}, {expression}, {location}, {lighting}"
        
        clothing_state_formatted = CLOTHING_STATES['sfw_covered'].format(OUTFIT_SFW=outfit)
        # Note: In the user snippet, CLOTHING_STATES['sfw_covered'] has {OUTFIT_SFW}, so we format that first or pass it up.
        # But variable_content also has 'wearing {outfit}'. This might be redundant if CLOTHING_STATE also says it.
        # Let's follow the template strictly. 
        # FIXED_BASE has {CLOTHING_STATE} and {VARIABLE_CONTENT}.
        # CLOTHING_STATE["sfw_covered"] is "fully covered, wearing {OUTFIT_SFW}".
        # VARIABLE_CONTENT example: "wearing {outfit}, {pose}..." -> This repeats "wearing {outfit}".
        # I will adjust variable_content to NOT include "wearing {outfit}" if clothing_state already handles it, 
        # OR just strictly follow the user snippet which had "wearing {outfit}" in variable_content AND "fully covered" in CLOTHING_STATE.
        # Looking at user code: 
        # _generate_sfw: CLOTHING_STATE="fully covered" (hardcoded string in call), OUTFIT not passed to template but used in variable_content.
        # BUT the definition of CLOTHING_STATES["sfw_covered"] was "fully covered, wearing {OUTFIT_SFW}".
        # I will follow the _generate_sfw implementation provided:
        # It calls self.base.format(CLOTHING_STATE="fully covered", VARIABLE_CONTENT="wearing {outfit}...")
        
        # Camera Logic
        cam_angle = kwargs.get('camera_angle') or random.choice(self.camera_angles)
        cam_lens = kwargs.get('camera_lens') or random.choice(self.camera_lenses)

        return base_template.format(
            HAIR_VARIATION=hair,
            BREAST_SIZE=breast,
            CLOTHING_STATE="fully covered",
            VARIABLE_CONTENT=variable_content,
            CAMERA_ANGLE=cam_angle,
            CAMERA_LENS=cam_lens
        ), {
            "hair": hair,
            "outfit": outfit,
            "location": location,
            "pose": pose,
            "expression": expression
        }
    
    def _generate_tease(self, category, manual_override=None, profile=None, **kwargs):
        manual_override = manual_override or {}
        base_template = self._build_base_string(profile)
        
        hair = manual_override.get('hair') or random.choice(HAIR_STYLES)
        breast = BREAST_SIZES["nsfw_medium"]
        
        outfit = _generate_outfit_string(manual_override) # Use same logic for tease for now, or specialize later
        if manual_override.get('outfit'):
             outfit = manual_override['outfit']
        
        location = manual_override.get('location') or random.choice(LOCATIONS['indoor_elegant'])
        pose = manual_override.get('pose') or random.choice(POSES['standing'])
        expression = random.choice(EXPRESSIONS['seductive'])
        lighting = random.choice(LIGHTING['dramatic'])
        
        if category == "with_male":
            interaction = random.choice(MALE_INTERACTIONS['body_contact'])
            variable_content = f"{pose}, {expression}, {location}, {lighting}, {interaction}"
        else:
             variable_content = f"{pose}, {expression}, {location}, {lighting}"
        
        # Used defined clothing state template
        clothing_state = CLOTHING_STATES['tease'].format(OUTFIT_TEASE=outfit)
        
        # Camera Logic
        cam_angle = kwargs.get('camera_angle') or random.choice(self.camera_angles)
        cam_lens = kwargs.get('camera_lens') or random.choice(self.camera_lenses)

        return base_template.format(
            HAIR_VARIATION=hair,
            BREAST_SIZE=breast,
            CLOTHING_STATE=clothing_state,
            VARIABLE_CONTENT=variable_content,
            CAMERA_ANGLE=cam_angle,
            CAMERA_LENS=cam_lens
        ), {
            "hair": hair,
            "outfit": outfit,
            "location": location,
            "pose": pose,
            "expression": expression
        }
    
    def _generate_nsfw_moderate(self, category, manual_override=None, profile=None, **kwargs):
        manual_override = manual_override or {}
        base_template = self._build_base_string(profile)
        
        hair = manual_override.get('hair') or random.choice(HAIR_STYLES)
        breast = BREAST_SIZES["nsfw_large"]
        
        outfit = _generate_outfit_string(manual_override)
        if manual_override.get('outfit'):
             outfit = manual_override['outfit']
        
        location = manual_override.get('location') or random.choice(LOCATIONS['indoor_cozy'])
        pose = manual_override.get('pose') or random.choice(POSES['lying'])
        expression = random.choice(EXPRESSIONS['intense'])
        lighting = random.choice(LIGHTING['artificial'])
        
        variable_content = f"{pose}, {expression}, {location}, {lighting}"
        if category == "with_male":
             variable_content += f", {random.choice(MALE_INTERACTIONS['touch_breasts'])}"

        clothing_state = CLOTHING_STATES['nsfw_partial'].format(OUTFIT_PARTIAL=outfit)
        
        # Camera Logic
        cam_angle = kwargs.get('camera_angle') or random.choice(self.camera_angles)
        cam_lens = kwargs.get('camera_lens') or random.choice(self.camera_lenses)

        return base_template.format(
            HAIR_VARIATION=hair,
            BREAST_SIZE=breast,
            CLOTHING_STATE=clothing_state,
            VARIABLE_CONTENT=variable_content,
            CAMERA_ANGLE=cam_angle,
            CAMERA_LENS=cam_lens
        ), {
            "hair": hair,
            "outfit": outfit,
            "location": location,
            "pose": pose,
            "expression": expression
        }
    
    def _generate_nsfw_extreme(self, category, manual_override=None, profile=None, **kwargs):
        manual_override = manual_override or {}
        base_template = self._build_base_string(profile)
        
        hair = manual_override.get('hair') or random.choice(HAIR_STYLES)
        breast = BREAST_SIZES["nsfw_large"]
        
        # Location logic
        location = manual_override.get('location')
        if not location:
            if category == 'fantasy':
                location = random.choice(LOCATIONS['fantasy'])
            else:
                location = random.choice(LOCATIONS['indoor_cozy'] + LOCATIONS['indoor_elegant'])
            
        pose = manual_override.get('pose') or random.choice(POSES['lying'])
        expression = random.choice(EXPRESSIONS['pleasure'])
        lighting = random.choice(LIGHTING['dramatic'])
        
        variable_content = f"{pose}, {expression}, {location}, {lighting}"
        
        # Fantasy additions
        if category == 'fantasy':
            race = kwargs.get('race', 'werewolf')
            if race in FANTASY_RACES:
                race_data = FANTASY_RACES[race]
                variable_content += f", with {race_data['features']}, {race_data['hands']} {random.choice(MALE_INTERACTIONS['touch_breasts'])}, {race_data['description']}"
        
        clothing_state = CLOTHING_STATES['nsfw_full']
        
        # Camera Logic
        cam_angle = kwargs.get('camera_angle') or random.choice(self.camera_angles)
        cam_lens = kwargs.get('camera_lens') or random.choice(self.camera_lenses)

        return base_template.format(
            HAIR_VARIATION=hair,
            BREAST_SIZE=breast,
            CLOTHING_STATE=clothing_state,
            VARIABLE_CONTENT=variable_content,
            CAMERA_ANGLE=cam_angle,
            CAMERA_LENS=cam_lens
        ), {
            "hair": hair,
            "outfit": "Nude",
            "location": location,
            "pose": pose,
            "expression": expression
        }

    def _build_full_prompt(self, character_id, variable_content, exposure=None, profile=None, **kwargs):
        """Helper to assemble full prompt with overrides"""
        base_template = self._build_base_string(profile)
        
        # dummy defaults if not provided in caller
        hair = "long straight black hair"
        breast = BREAST_SIZES["nsfw_medium"]
        clothing_state = "fully nude"
        
        if exposure:
             # Tuple (top_state, bottom_state)
             clothing_state = f"{exposure[0]}, {exposure[1]}"
             
        # Camera Logic (Override or Random)
        cam_angle = kwargs.get('camera_angle')
        if not cam_angle or cam_angle == "random":
            cam_angle = random.choice(self.camera_angles)
            
        cam_lens = kwargs.get('camera_lens')
        if not cam_lens or cam_lens == "random":
             cam_lens = random.choice(self.camera_lenses)

        return base_template.format(
            HAIR_VARIATION=hair,
            BREAST_SIZE=breast,
            CLOTHING_STATE=clothing_state,
            VARIABLE_CONTENT=variable_content,
            CAMERA_ANGLE=cam_angle,
            CAMERA_LENS=cam_lens
        )

    def generate_transformation_prompt(self, character_id, race, level, **kwargs):
        """
        Generate a race transformation prompt.
        """
        # Note: In a real integration we should fetch the profile object using character_id.
        # But PromptGenerator is standalone. We assume caller passes profile or we use defaults.
        # For this standalone version we will simulate profile behavior if needed.
        
        transformation = self.transformations.get(race)
        if not transformation:
            raise ValueError(f"Race {race} not found")
            
        special_features = transformation['special_features']
        hair_change = transformation['hair_change'] or "long hair"
        
        prompt = f"(masterpiece), (best quality), beautiful young Korean woman turned into {race}, {special_features}, {hair_change}, detailed eyes, {kwargs.get('pose', 'standing')}, detailed background"
        
        return {
            'positive': prompt,
            'negative': self.negative['fantasy'],
            'metadata': {'type': 'transformation', 'race': race}
        }
    
    def generate_masturbation_prompt(self, character_id, hand_config, position, location, exposure_level, **kwargs):
        """
        Generate detailed masturbation prompt.
        """
        action_data = self.masturbation_actions['hand_positions'][hand_config]
        position_data = self.masturbation_actions['body_positions'][position]
        exposure_data = self.clothing_exposures.get(exposure_level)
        
        # Hand Logic
        if hand_config == "one_hand_breast_one_hand_clit":
            side = random.choice(["left", "right"])
            breast_action = action_data['breast_hand'].format(SIDE=side)
            lower_action = action_data['lower_hand']
        elif "breast" in hand_config:
             breast_action = "squeezing breasts"
             lower_action = "fingering"
        else:
             breast_action = "hands elsewhere"
             lower_action = "fingering"
        
        # Position Logic
        body_position = position_data['description']
        position_variation = random.choice(position_data.get('variations', ['']) or [''])
        
        # Exposure Logic
        top_state, bottom_state = "nude", "nude"
        if exposure_data:
            if exposure_level == "partial_exposure_single_nipple":
                side = random.choice(["left", "right"])
                direction = random.choice(exposure_data['directions'])
                top_state = exposure_data['top'].format(TOP="shirt", SIDE=side)
                bottom_state = exposure_data['bottom'].format(DIRECTION=direction)
            elif exposure_level == "no_exposure_hands_inside":
                top_state = exposure_data['top'].format(TOP="sweater")
                bottom_state = exposure_data['bottom'].format(BOTTOM="pants")

        variable_content = f"{body_position} {position_variation}, {breast_action}, {lower_action}, {location}, sweat, flushed face"
        
        clothing_str = f"{top_state}, {bottom_state}"
        
        # Simple construction for now
        prompt = f"(masterpiece), (best quality), beautiful young Korean woman, {clothing_str}, {variable_content}, depth of field"
        
        return {
             'positive': prompt,
             'negative': self.negative['nsfw'],
             'metadata': {'type': 'masturbation', 'hand_config': hand_config}
        }
    
    def generate_public_masturbation_prompt(self, character_id, public_location, **kwargs):
        """
        Generate public masturbation prompt with tension.
        """
        location_data = None
        for category in self.public_locations.values():
            if public_location in category:
                location_data = category[public_location]
                break
        
        if not location_data:
            # Fallback
            location_data = list(self.public_locations['outdoor_public'].values())[0]
            public_location = "park"
        
        time = random.choice(location_data['time'])
        atmosphere = location_data['atmosphere']
        tension_expression = location_data['tension']
        
        kwargs['expression'] = tension_expression
        kwargs['location'] = f"{public_location} at {time}"
        
        # Delegate to main masturbation gen (simplified args for demo)
        base = self.generate_masturbation_prompt(
            character_id=character_id, 
            hand_config=kwargs.get("hand_config", "one_hand_breast_one_hand_clit"),
            position=kwargs.get("position", "standing"),
            location=f"{public_location}, {atmosphere}",
            exposure_level=kwargs.get("exposure_level", "no_exposure_hands_inside")
        )
        
        return base

# Utils for metadata
def generate_metadata(level, prompt_data=None):
    # Caption
    caption_list = CAPTIONS.get(level, CAPTIONS['sfw'])
    caption = random.choice(caption_list)
    
    # Hashtags
    tags = HASHTAGS['base'].copy()
    if level == 'sfw':
        tags += HASHTAGS.get('sfw_add', [])
    elif level == 'tease':
        tags += HASHTAGS.get('tease_add', [])
    
    return {
        'caption': caption,
        'hashtags': tags,
        'account': 'A' if level == 'sfw' else 'B',
        'patreon_tier': None if level == 'sfw' else ('T3' if level == 'tease' else 'T4')
    }

def validate_prompt(prompt, level):
    # Mandatory checks
    for must in VALIDATION_RULES["must_have"]:
        if must not in prompt:
            return False, f"Missing required element: {must}"
    
    # SFW checks
    if level == "sfw":
        for forbidden in VALIDATION_RULES["must_not_have_sfw"]:
            if forbidden in prompt.lower():
                return False, f"Forbidden element in SFW: {forbidden}"
    
    # Length check
    if len(prompt) > VALIDATION_RULES["max_length"]:
        return False, f"Prompt too long ({len(prompt)} > {VALIDATION_RULES['max_length']})"
    
    return True, "Valid"

if __name__ == "__main__":
    # Simple test if run directly
    gen = PromptGenerator()
    p = gen.generate(level="sfw", count=1)[0]
    print("Test Prompt:", p['positive'])
