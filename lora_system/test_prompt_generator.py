
from prompt_generator import PromptGenerator, generate_metadata, validate_prompt

def run_tests():
    generator = PromptGenerator()
    
    print("\n=== Testing SFW Generation ===")
    sfw_prompts = generator.generate(level="sfw", category="general", count=2)
    for p in sfw_prompts:
        prompt_text = p['positive']
        print(f"[SFW] {prompt_text[:100]}...")
        
        # Validation
        is_valid, msg = validate_prompt(prompt_text, "sfw")
        print(f"Validation: {msg}")
        
        # Metadata
        meta = generate_metadata("sfw", p)
        print(f"Metadata: {meta['hashtags'][:3]}...")

    print("\n=== Testing Tease Generation (With Male) ===")
    tease_prompts = generator.generate(level="tease", category="with_male", count=2)
    for p in tease_prompts:
        print(f"[Tease] {p['positive'][:100]}...")
        is_valid, msg = validate_prompt(p['positive'], "tease")
        print(f"Validation: {msg}")

    print("\n=== Testing NSFW Extreme (Fantasy) ===")
    fantasy_prompts = generator.generate(level="nsfw_extreme", category="fantasy", count=2, race="elf")
    for p in fantasy_prompts:
        print(f"[Fantasy] {p['positive'][:100]}...")
        is_valid, msg = validate_prompt(p['positive'], "nsfw_extreme")
        print(f"Validation: {msg}")

if __name__ == "__main__":
    run_tests()
