# Firestore Schema Design for Seoyeon Project

## 1. Collection: `system_config`
Global configuration settings for the agent.

### Document: `visual_guideline`
- **base_positive_prompt** (string): "(masterpiece, best quality, ultra detailed, photorealistic), delicate Korean woman, soft expression, loose softly waved jet-black long hair, no bangs, natural makeup, smooth radiant Korean skin tone with subtle warmth, slim toned body, narrow waist, feminine proportions, natural large soft breasts with realistic slight sag, delicate collarbone and shoulder definition, graceful posture and balanced silhouette, natural photogenic harmony across all expressions"
- **base_negative_prompt** (string): "lowres, worst quality, blurry, jpeg artifacts, deformed, distorted, mutated, bad anatomy, bad proportions, extra arms, extra hands, extra legs, extra fingers, two faces, two heads, duplicate person, mirror reflection, mirrored face, mirrored body, text, watermark, signature, hair covering eyes, bangs, thick bangs, split bangs"

## 2. Collection: `wardrobe`
Digital wardrobe inventory.

### Document Fields (List of Items)
Each document represents a clothing item or the collection contains documents for each item.
- **id** (string): Unique identifier.
- **name** (string): Display name of the item.
- **tags** (array): Keywords describing the style/vibe (e.g., ["청순", "가을", "데이트"]).
- **last_worn_date** (timestamp/string): Date when last used in content generation.

## 3. Collection: `daily_feed`
Log of daily generated content.

### Document Fields
- **date** (string/timestamp): Key for the entry.
- **mood** (string): Overview of the day's mood.
- **concept** (string): Concept title or description.
- **final_prompt** (string): The full image generation prompt used.
- **caption_text** (string): The generated caption.
