import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from services.image_gen import ImageGenerator
import datetime

def generate_image_replicate(prompt: str, seed: int = None) -> str:
    """
    [기능]
    1. Flux 모델로 서연이 고화질 이미지 생성 (Using ImageGenerator Service)
    2. 로컬 폴더에 이미지 자동 다운로드
    3. 작업 내용을 로그 파일에 기록
    """
    
    result_path, image_url, used_seed = ImageGenerator.generate(prompt, seed=seed, prefix_seoyeon=True)
    
    if not result_path:
        return "Error: Generation failed."

    # 5. 로그 기록 (activity_log.md)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(result_path)
    
    log_entry = f"""
## [{timestamp}] Generation Log
- **Prompt:** {prompt}
- **File:** {filename}
- **Status:** Success
- **URL:** {image_url}
---
"""
    with open("activity_log.md", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

    return f"Image saved to: {result_path} (Log updated)"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Hi-Res Image with Auto-Download & Logging")
    parser.add_argument("--prompt", type=str, required=True, help="Image prompt")
    parser.add_argument("--seed", type=int, default=None, help="Specific seed")
    args = parser.parse_args()
    
    result = generate_image_replicate(args.prompt, args.seed)
    print(result)
