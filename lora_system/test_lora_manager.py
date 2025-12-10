
from lora_manager import (
    MultiCharacterPromptGenerator, 
    add_new_character, 
    CharacterComparator, 
    CharacterVersionManager,
    CHARACTER_PROFILES
)

def run_test():
    # 1. Initialization
    print("\n=== Initializing Generator ===")
    generator = MultiCharacterPromptGenerator()
    print("Available characters:", generator.list_characters())

    # 2. Generating Prompts
    print("\n=== Generating Seoyeon SFW Batch ===")
    seoyeon_sfw = generator.generate_batch(
        character_id="seoyeon",
        level="sfw",
        category="general",
        count=3
    )
    for p in seoyeon_sfw:
        print(f"Prompt {p['metadata']['batch_index']}: {p['positive'][:100]}...")

    print("\n=== Generating Minjee Tease Batch (Custom Hair) ===")
    minjee_tease = generator.generate_batch(
        character_id="minjee",
        level="tease",
        category="general",
        count=2,
        hair_texture="soft waves",
        hair_state="loose"
    )
    for p in minjee_tease:
        print(f"Prompt {p['metadata']['batch_index']}: {p['positive'][:100]}...")

    print("\n=== Generating Yuna Fantasy Batch ===")
    yuna_fantasy = generator.generate_batch(
        character_id="yuna",
        level="nsfw_extreme",
        category="fantasy",
        count=2,
        race="elf",
        breast_size="medium"
    )
    for p in yuna_fantasy:
        print(f"Prompt {p['metadata']['batch_index']}: {p['positive'][:100]}...")

    # 3. Adding New Character
    print("\n=== Adding New Character: Jihyo ===")
    new_character = {
        "id": "jihyo_v1",
        "name": "Jihyo",
        "lora_trigger": "jihyo",
        "fixed_base": {
            "ethnicity": "Korean",
            "face_type": "Korean idol face",
            "age_range": "mid 20s",
            "skin_tone": "warm tan skin",
            "facial_features": "round soft features, bright eyes",
            "makeup_style": "natural glowy makeup",
            "hair_color": "brown",
            "hair_length": "long",
            "bangs": "see-through bangs",
            "forehead": "partially visible",
            "body_type": "curvy body"
        },
        "variable_attributes": {
            "hair_texture": ["wavy", "straight", "curly"],
            "hair_state": ["loose", "half-up", "ponytail"],
            "breast_size_options": ["medium-large", "large"],
            "body_state": ["curvy", "athletic"]
        },
        "constraints": {
            "prohibited_hair": ["very short", "blonde"],
            "prohibited_features": ["childlike", "thin"],
            "age_constraint": "must_be_adult"
        },
        "quality_preset": {
            "masterpiece": 1.3,
            "best_quality": 1.3,
            "detail_level": "ultra detailed",
            "photo_type": "8k RAW photo",
            "render_style": "photorealistic"
        }
    }
    
    char_id = add_new_character(new_character)
    
    # Re-init generator to pick up new char
    generator = MultiCharacterPromptGenerator()
    
    jihyo_prompts = generator.generate_batch(char_id, "sfw", "general", count=2)
    print(f"Generated {len(jihyo_prompts)} prompts for Jihyo.")

    # 4. Comparison
    print("\n=== Comparing Seoyeon vs Minjee ===")
    comparator = CharacterComparator(generator)
    diff = comparator.compare_characters("seoyeon", "minjee")
    print("Visual Differences (sample):", list(diff['visual'].keys())[:2])

    # 5. Version Management
    print("\n=== Creating Seoyeon v2 ===")
    version_manager = CharacterVersionManager()
    seoyeon_v2_id = version_manager.create_new_version(
        base_character_id="seoyeon",
        version_number="v2",
        changes={
            'fixed_base': {
                'age_range': 'mid 20s',
                'facial_features': 'mature sharp features, piercing eyes'
            }
        }
    )
    print(f"Created version: {seoyeon_v2_id}")
    
    # Verify new version works
    generator = MultiCharacterPromptGenerator() # Update generator
    v2_prompts = generator.generate_batch(seoyeon_v2_id, "sfw", "general", count=1)
    print(f"V2 Prompt: {v2_prompts[0]['positive'][:100]}...")

if __name__ == "__main__":
    run_test()
