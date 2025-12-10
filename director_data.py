# director_data.py
# static strings and configuration data for VPS Director

# ==========================================
# 1. FIXED PROMPT BASES
# ==========================================
PROMPT_QUALITY = "(masterpiece:1.3), (best quality:1.3), ultra detailed, 8k RAW photo, photorealistic, sharp focus, extremely detailed face, realistic skin texture, pore details, professional studio lighting"

# Removed "natural minimal makeup" to allow variable makeup control
PROMPT_SUBJECT = "beautiful young Korean woman, Korean idol face, early 20s, fair skin, delicate sharp features, huge clear eyes"

PROMPT_BODY = "slim body, natural large soft breasts with realistic slight sag, soft pendulous breasts"

PROMPT_HAIR_BASE = "long straight black hair" 

# User-defined Negative Prompt
NEGATIVE_PROMPT = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, deformed, ugly, mutilated, out of frame, extra limbs, poorly drawn face, poorly drawn hands, mutation, deformed hands, long body, bad proportions"

# ==========================================
# 2. SELECTION DATA
# ==========================================

SHOT_TYPES = {
    "얼굴 클로즈업 (Extreme Close-up)": "extreme close-up of face, macro lens, detailed eyes",
    "상반신 (Upper Body)": "upper body shot, portrait photography",
    "허벅지샷 (Cowboy Shot)": "cowboy shot, thighs up, american shot",
    "전신 (Full Body)": "full body shot, showing shoes, wide angle",
}

ANGLES_DICT = {
    "(기본) 눈높이": "eye level angle",
    "로우 앵글 (다리 길게)": "low angle, from below",
    "하이 앵글 (얼짱 각도)": "high angle, looking up at camera, cute perspective",
    "사선 (Dutch Angle)": "dutch angle, dynamic composition",
    "뒤에서 (Back View)": "view from behind, back shot",
    "거울 셀카 (Selfie)": "mirror selfie, holding phone, looking at mirror",
    "탑 뷰 (Top View)": "overhead view, bird's eye view",
    "사이드 뷰 (Side Profile)": "side profile, looking away"
}

LENS_DICT = {
    "85mm (여친렌즈)": "85mm lens, depth of field, bokeh",
    "105mm (매크로)": "105mm macro lens, extreme detail",
    "50mm (표준)": "50mm lens, natural look",
    "35mm (스냅)": "35mm lens, street photography style",
    "24mm (광각)": "24mm lens, dynamic background",
    "16mm (초광각)": "16mm ultra wide lens, distortion"
}

LIGHTING_DICT = {
    "(기본) 자연광": "natural lighting, soft sunlight",
    "스튜디오 (부드러운)": "soft studio lighting, rim light, professional photography",
    "어두운/밤 (Cinematic)": "cinematic lighting, dim lighting, moody atmosphere, volumetric fog",
    "네온 (Cyberpunk)": "neon lights, colorful lighting, cyberpunk vibes",
    "골든 아워 (노을)": "golden hour, sunset lighting, warm tone",
    "플래시 (파파라치)": "camera flash, hard lighting, night photography"
}

LOGIC_MAP = {
    "얼굴 클로즈업 (Extreme Close-up)": {
        "angles": ["(기본) 눈높이", "하이 앵글 (얼짱 각도)", "사선 (Dutch Angle)", "사이드 뷰 (Side Profile)"],
        "lens": ["105mm (매크로)", "85mm (여친렌즈)"],
        "default_lens": "105mm (매크로)"
    },
    "상반신 (Upper Body)": {
        "angles": ["(기본) 눈높이", "하이 앵글 (얼짱 각도)", "로우 앵글 (다리 길게)", "거울 셀카 (Selfie)", "뒤에서 (Back View)"],
        "lens": ["85mm (여친렌즈)", "50mm (표준)", "35mm (스냅)"],
        "default_lens": "85mm (여친렌즈)"
    },
    "허벅지샷 (Cowboy Shot)": {
        "angles": ["(기본) 눈높이", "로우 앵글 (다리 길게)", "사선 (Dutch Angle)", "사이드 뷰 (Side Profile)"],
        "lens": ["50mm (표준)", "35mm (스냅)", "85mm (여친렌즈)"],
        "default_lens": "50mm (표준)"
    },
    "전신 (Full Body)": {
        "angles": ["로우 앵글 (다리 길게)", "(기본) 눈높이", "탑 뷰 (Top View)", "사선 (Dutch Angle)", "뒤에서 (Back View)"],
        "lens": ["24mm (광각)", "35mm (스냅)", "16mm (초광각)"],
        "default_lens": "24mm (광각)"
    }
}

HAIRSTYLES_DICT = {
    "(기본) 긴 생머리 (Long Straight)": "no bangs, forehead fully exposed",
    "웨이브 펌 (Long Wavy)": "wavy texture, voluminous",
    "포니테일 (Ponytail)": "tied back high ponytail",
    "똥머리 (Bun)": "hair bun, messy bun",
    "단발 (Bob Cut)": "bob cut style",
    "반묶음 (Half-up)": "half-up half-down style",
    "양갈래 (Twin Tails)": "twintails, cute style"
}
HAIRSTYLES = list(HAIRSTYLES_DICT.keys())

# New: Facial Expressions (Display -> Prompt)
EXPRESSIONS_DICT = {
    "(기본) 무표정/시크": "neutral expression, chic slight smile, closed mouth",
    "활짝 웃음 (Bright)": "bright smile, showing teeth, happy expression",
    "유혹적 (Seductive)": "seductive smile, slightly parted lips, sultry gaze",
    "몽환적 (Dreamy)": "dreamy looking, soft gaze, slightly open mouth",
    "놀람/부끄 (Shy)": "shy blushing, surprised expression",
    "도도함 (Arrogant)": "arrogant look, looking down, confident"
}
EXPRESSIONS = list(EXPRESSIONS_DICT.keys())

OUTFITS_DICT = {
    "Casual": {
        "흰색 티셔츠 & 청바지": "wearing white t-shirt, blue jeans",
        "오버핏 후드티": "wearing oversized hoodie",
        "크롭탑 & 트레이닝 팬츠": "wearing crop top, sweatpants",
        "베이지색 니트": "wearing beige knit sweater",
        "검정색 가죽 자켓": "wearing black leather jacket, chic style",
        "체크무늬 셔츠 (레이어드)": "wearing plaid shirt layered over white tee",
        "민소매 탑 & 반바지": "wearing sleeveless top, denim shorts",
        "바시티 자켓 (스쿨룩)": "wearing varsity jacket, casual sporty look",
        "멜빵 바지 (귀여운)": "wearing denim overall pants, cute style",
        "스트라이프 티셔츠": "wearing striped t-shirt, casual look",
        "가디건 & 롱스커트": "wearing soft cardigan, long skirt, cozy look",
        "오프숄더 니트": "wearing off-shoulder knit sweater",
        "트랙탑 저지 (Y2K)": "wearing track top jersey, y2k fashion",
        "크롭 가디건 세트": "wearing crop cardigan set"
    },
    "Date": {
        "오프숄더 원피스": "wearing off-shoulder dress",
        "실크 블라우스 & 스커트": "wearing sheer white blouse slightly unbuttoned at top",
        "트위드 자켓 셋업": "wearing tweed jacket, matching skirt",
        "꽃무늬 쉬폰 드레스": "wearing floral chiffon dress",
        "블랙 미니 드레스": "wearing black mini dress, elegant",
        "화이트 레이스 원피스": "wearing white lace dress, innocent look",
        "새틴 슬립 드레스": "wearing satin slip dress, glamorous",
        "랩 원피스 (우아한)": "wearing wrap dress, elegant silhouette",
        "뷔스티에 원피스": "wearing bustier dress",
        "벨벳 드레스": "wearing velvet dress, luxurious",
        "시스루 파티룩": "wearing see-through party dress, alluring",
        "홀터넥 드레스": "wearing halterneck dress, showing shoulders",
        "니트 원피스 (몸매강조)": "wearing tight knit dress, body hugging",
        "레드 칵테일 드레스": "wearing red cocktail dress"
    },
    "Summer": {
        "비키니 (트로피컬)": "wearing tropical print bikini",
        "래쉬가드 & 보드숏": "wearing rash guard, board shorts",
        "모노키니 (블랙)": "wearing black monokini",
        "화이트 셔츠 (비치룩)": "wearing white oversized shirt, beach wear",
        "튜브탑 비키니": "wearing tube top bikini",
        "마이크로 비키니 (레드)": "wearing red micro bikini",
        "크로셰 비키니 (보헤미안)": "wearing crochet bikini, bohemian style",
        "하와이안 셔츠 셋업": "wearing hawaiian shirt, matching shorts",
        "스윔수트 (컷아웃)": "wearing cutout one-piece swimsuit",
        "비치 원피스 (맥시)": "wearing maxi beach dress",
        "데님 핫팬츠 & 브라탑": "wearing denim hot pants, bra top",
        "시스루 로브 & 비키니": "wearing see-through robe over bikini",
        "스쿨 미즈 (네이비)": "wearing navy school swimsuit",
        "체크무늬 비키니": "wearing plaid pattern bikini"
    },
    "Home": {
        "실크 잠옷 (네이비)": "wearing navy silk pajamas",
        "박시한 셔츠 (하의실종)": "wearing oversized shirt, no pants",
        "귀여운 동물 잠옷": "wearing cute animal pajamas",
        "슬립 드레스": "wearing slip dress",
        "후드 집업 & 속옷": "wearing hoodie zip-up, underwear",
        "탱크탑 & 돌핀팬츠": "wearing tank top, dolphin shorts",
        "샤워 가운 (호텔)": "wearing bathrobe",
        "벨벳 트레이닝 셋업": "wearing velvet tracksuit",
        "레이스 란제리 (화이트)": "wearing white lace lingerie",
        "스포츠 브라 & 레깅스": "wearing sports bra, leggings",
        "니트 가디건 (루즈핏)": "wearing loose knit cardigan laundry day",
        "캐미솔 & 숏팬츠": "wearing camisole top, short pants",
        "남자친구 셔츠": "wearing boyfriend's shirt",
        "수면 잠옷 (파스텔)": "wearing fluffy pastel pajamas"
    },
    "Special": {
        "교복 (네이비)": "wearing navy school uniform",
        "메이드복": "wearing maid outfit",
        "경찰 제복": "wearing police uniform",
        "한복 (파스텔)": "wearing pastel hanbok, korean traditional clothes",
        "간호사 코스튬": "wearing nurse outfit, costume",
        "바니걸 (블랙)": "wearing black bunny girl outfit",
        "승무원 유니폼": "wearing flight attendant uniform",
        "치어리더": "wearing cheerleader outfit",
        "테니스복": "wearing tennis outfit, skirt",
        "발레복 (튜튜)": "wearing ballet tutu, leotard",
        "요가복 (필라테스)": "wearing yoga outfit, pilates",
        "레이싱 모델": "wearing racing model outfit",
        "오피스룩 (정장)": "wearing office suit, pencil skirt, glasses",
        "산타걸 (크리스마스)": "wearing santa girl costume"
    }
}
# Storyboard Themes (Random Scenarios)
STORY_THEMES = [
    "Summer Beach Vacation Vlog: Walking on the sand, playing with water, sunset dinner",
    "K-pop Music Video Shoot: Behind the scenes, makeup retouch, monitoring the camera",
    "Luxury Hotel Staycation: Waking up, breakfast in bed, swimming in the pool, champagne night",
    "University Student Vibe: Library study session, campus walk, coffee break with friends",
    "Secret Date at Night: Walking in the park, hiding from paparazzi, car date",
    "Fitness & Pilates Routine: Stretching, doing yoga poses, drinking protein shake, mirror selfie",
    "Cozy Home Date: Cooking pasta together, watching movies on the sofa, wearing oversized hoodies",
    "Airport Fashion (Departure): Walking into the terminal, waving to fans, passport check",
    "Fan Meeting Event: Signing albums, wearing animal headbands, making heart gestures",
    "Practice Room Dance Rehearsal: Sweating after practice, sitting on the floor, group selfie",
    "Winter Ski Resort Trip: Drinking hot cocoa, wearing ski gear, playing with snow",
    "Han River Picnic: Eating ramen, riding a bicycle, sunset view",
    "Cafe Tour Date: Eating strawberry cake, drinking iced latte, taking photos for instagram"
]

OUTFITS = {k: list(v.keys()) for k, v in OUTFITS_DICT.items()}

TRANSLATIONS = {
    "KR": {
        "title": "가상 화보 촬영실 (Director Mode)",
        "sidebar_title": "VPS Director",
        "section_mode": "모드 (Mode)",
        "section_engine": "엔진 (Engine)",
        "section_view": "뷰 (View)",
        "mode_single": "단일 촬영 (Single)",
        "mode_story": "스토리보드 (Campaign)",
        "engine_local": "로컬 (ComfyUI)",
        "engine_cloud": "클라우드 (Replicate)",
        "toggle_monitor": "모니터 패널 (Monitor)",
        "btn_random": "랜덤 설정 (Random)",
        "btn_folder": "폴더 열기",
        "header_settings": "촬영 설정 (Settings)",
        "header_camera": "카메라 & 앵글 (Smart Logic)",
        "label_shot": "1. 샷 구분 (Shot)",
        "label_lens": "2. 렌즈 (Lens)",
        "label_angle": "3. 앵글 (Angle)",
        "label_light": "4. 조명 (Light)",
        "header_style": "스타일링",
        "label_hair": "헤어",
        "label_face": "표정 & 메이크업",
        "label_expression": "표정",
        "label_makeup": "메이크업 (텍스트)",
        "label_outfit_cat": "의상 카테고리",
        "label_outfit": "의상",
        "placeholder_outfit": "예: 시스루 블라우스",
        "label_acc_full": "신발/스타킹",
        "label_acc_close": "악세사리",
        "label_acc_gen": "악세사리",
        "header_action": "액션 & 배경",
        "label_action": "행동 지시",
        "btn_ai": "AI 추천",
        "label_location": "장소/배경",
        "tab_monitor": "촬영장 (Main)",
        "tab_gallery": "갤러리",
        "tab_log": "로그",
        "btn_preview": "프롬프트 미리보기 (Check)",
        "btn_shoot": "슛 (SHOOT)",
        "status_ready": "**Ready:**",
        "msg_ready": "👈 설정을 마치고 '미리보기'를 누르세요.",
        "status_shooting": "촬영 중",
        "header_info": "촬영 정보",
        "label_neg": "Negative Prompt (공통)",
        "header_planning": "기획 설정 (Planning)",
        "label_theme": "주제 (Theme)",
        "label_platform": "게시 플랫폼",
        "label_shots": "컷 수 (Shots)",
        "btn_generate_plan": "AI 시나리오 생성",
        "status_thinking": "AI 감독이 시나리오를 구상 중입니다... (Thinking)",
        "header_cue_sheet": "큐시트 (Cue Sheet)",
        "help_ai_action": "랜덤 행동 생성"
    },
    "EN": {
        "title": "Virtual Photo Studio (Director Mode)",
        "sidebar_title": "VPS Director",
        "section_mode": "Mode",
        "section_engine": "Engine",
        "section_view": "View",
        "mode_single": "Single Shot",
        "mode_story": "Campaign (Storyboard)",
        "engine_local": "Local (ComfyUI)",
        "engine_cloud": "Cloud (Replicate)",
        "toggle_monitor": "Show Monitor Panel",
        "btn_random": "Random Config",
        "btn_folder": "Open Folder",
        "header_settings": "Configurations",
        "header_camera": "Camera & Angle",
        "label_shot": "1. Shot Type",
        "label_lens": "2. Lens",
        "label_angle": "3. Angle",
        "label_light": "4. Lighting",
        "header_style": "Styling",
        "label_hair": "Hairstyle",
        "label_face": "Expression & Makeup",
        "label_expression": "Expression",
        "label_makeup": "Makeup (Text)",
        "label_outfit_cat": "Outfit Category",
        "label_outfit": "Outfit",
        "placeholder_outfit": "e.g. See-through blouse",
        "label_acc_full": "Shoes/Stockings",
        "label_acc_close": "Accessories",
        "label_acc_gen": "Accessories",
        "header_action": "Action & Background",
        "label_action": "Action Prompt",
        "btn_ai": "AI Idea",
        "label_location": "Location",
        "tab_monitor": "Monitor",
        "tab_gallery": "Gallery",
        "tab_log": "Log",
        "btn_preview": "Preview Prompt",
        "btn_shoot": "SHOOT",
        "status_ready": "**Ready to Shoot:**",
        "msg_ready": "Click 'Preview' when ready.",
        "status_shooting": "Shooting",
        "header_info": "Info",
        "label_neg": "Negative Prompt (Global)",
        "header_planning": "Planning",
        "label_theme": "Theme",
        "label_platform": "Platform",
        "label_shots": "Shots",
        "btn_generate_plan": "Generate Plan",
        "status_thinking": "AI Director is planning...",
        "header_cue_sheet": "Cue Sheet",
        "help_ai_action": "Generate Random Action"
    }
}
