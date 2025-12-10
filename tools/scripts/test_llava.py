import replicate
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("REPLICATE_API_TOKEN")
print(f"Token: {token[:5]}..." if token else "Token: None")

try:
    # Test with a dummy image URL or local file if possible
    # Using a public image for testing
    output = replicate.run(
        "yorickvp/llava-13b:b5f6212d03250f3b8869c53ab7995bd28a5033273e9790692dcc9a4d872146f4",
        input={
            "image": "https://replicate.delivery/pbxt/IJZpO0iH9sfa9s2.jpg",
            "prompt": "Describe this image."
        }
    )
    print("Result:", "".join(output))
except Exception as e:
    print(f"Error: {e}")
