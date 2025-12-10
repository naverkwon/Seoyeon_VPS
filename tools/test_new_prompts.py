
import sys
import os

# Add root to data
sys.path.append(os.getcwd())

from lora_system.prompt_generator import PromptGenerator
# Need MultiCharacterPromptGenerator for Male/Duo
from lora_system.lora_manager import MultiCharacterPromptGenerator

def test_new_logic():
    gen = PromptGenerator()
    multi_gen = MultiCharacterPromptGenerator()
    
    print("\n--- 1. Transformation Test (Succubus) ---")
    try:
        res = gen.generate_transformation_prompt("seoyeon", "succubus", "nsfw_extreme")
        print(f"[POSITIVE] {res['positive']}")
    except Exception as e:
        print(f"[ERROR] {e}")

    print("\n--- 2. Public Masturbation Test (Han River) ---")
    try:
        res = gen.generate_public_masturbation_prompt(
            "seoyeon", 
            "han_river_park",
            hand_config="one_hand_breast_one_hand_clit",
            position="standing"
        )
        print(f"[POSITIVE] {res['positive']}")
    except Exception as e:
        print(f"[ERROR] {e}")

    print("\n--- 3. Male Solo Test (Jun) ---")
    try:
        res = multi_gen.generate_male_solo_prompt(
            "jun", 
            "one_hand_stroking",
            "lying_on_back",
            "hotel bed"
        )
        print(f"[POSITIVE] {res['positive']}")
    except Exception as e:
        print(f"[ERROR] {e}")

    print("\n--- 4. Duo Test (Seoyeon + Jun, Missionary) ---")
    try:
        res = multi_gen.generate_duo_prompt(
            "seoyeon",
            "jun",
            "missionary",
            "hotel bed"
        )
        print(f"[POSITIVE] {res['positive']}")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    test_new_logic()
