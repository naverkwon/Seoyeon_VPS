
# ==========================================
# Data Constants for Prompt Generation
# ==========================================

HAIR_STYLES = [
    # Straight
    "long damp straight black hair", "long silky straight black hair", "long straight black hair",
    "medium length straight black hair", "shoulder length straight black hair", "short bob cut straight black hair",
    "hime cut straight black hair", "sleek straight black hair",
    
    # Wavy
    "long wavy black hair", "loose wavy black hair", "voluminous wavy black hair",
    "body wave black hair", "beach waves black hair", "messy wavy black hair",
    
    # Styled
    "high ponytail black hair", "loose ponytail black hair", "twin tails black hair",
    "braided black hair", "french braid black hair", "side braid black hair",
    "half-up half-down black hair", "messy bun black hair", "neat bun black hair",
    "wet look back hair", "swept back black hair"
]

BREAST_SIZES = {
    "sfw_small": "natural small breasts",
    "sfw_medium": "natural medium breasts",
    "nsfw_medium": "natural medium-large soft breasts with realistic slight sag, soft pendulous breasts",
    "nsfw_large": "natural extra-large soft breasts with realistic heavy sag, soft pendulous breasts"
}

CLOTHING_STATES = {
    "sfw_covered": "fully covered, wearing {OUTFIT_SFW}",
    "tease": "wearing {OUTFIT_TEASE}",
    "nsfw_partial": "topless under {OUTFIT_PARTIAL}",
    "nsfw_full": "completely topless"
}

TOPS = [
    "white oversized t-shirt", "black crop top", "tight white tank top",
    "semi-sheer white blouse", "ribbed knit sweater", "silk camisole",
    "off-shoulder knitted top", "button-up white shirt", "sports bra",
    "lace bralette", "satin pajama top"
]

BOTTOMS = [
    "denim short shorts", "pleated mini skirt", "tight pencil skirt",
    "yoga leggings", "silk pajama shorts", "black lace panties",
    "white cotton panties", "string bikini bottom", "high-waisted jeans",
    "tennis skirt"
]

OUTERWEAR = [
    "oversized cardigan", "denim jacket", "leather jacket",
    "trench coat", "hoodie", "blazer"
]

FULL_BODY = [
    "fitted black cocktail dress", "tailored white blazer dress", "soft red wrap dress",
    "ivory silk slip dress", "floral summer dress", "black turtleneck bodysuit",
    "gym bodysuit", "uniform style dress"
]

POSES = {
    "sitting": [
        "sitting by cafe window", "sitting on couch", "sitting at desk",
        "sitting on bed", "sitting at dinner table"
    ],
    "standing": [
        "standing by window", "standing in lobby", "leaning against wall",
        "looking back over shoulder", "posing hands on hips", "walking down street"
    ],
    "lying": [
        "lying on bed back arched", "lying on stomach looking at camera", "lying sideways on sofa",
        "sprawled on bed messy sheets", "kneeling on bed"
    ],
    "transport": [
        "empty late-night bus back seat", "empty subway car", "private yacht deck"
    ],
    "fantasy": [
        "forest cabin", "spaceship interior", "ancient cave", "enchanted forest"
    ]
}

LOCATIONS = {
    "indoor_cozy": [
        "bedroom", "modern minimalist living room", "cozy cafe corner",
        "sunlit kitchen", "messy artist studio", "library stack",
        "modern kitchen counter", "marble bathroom", "steamy shower glass",
        "walk-in closet", "sunlit living room", "velvet sofa", "silk bedsheets"
    ],
    "indoor_elegant": [
        "hotel lobby", "restaurant booth", "art gallery", "penthouse suite",
        "private library", "opera box", "ballroom staircase", "wine cellar"
    ],
    "outdoor": [
        "rooftop terrace", "balcony", "outdoor cafe table", "rooftop pool",
        "private garden bench", "seaside cliff", "yacht deck", "botanical garden"
    ],
    "transport": [
        "empty late-night bus back seat", "empty subway car", "private yacht deck"
    ],
    "fantasy": [
        "forest cabin", "spaceship interior", "ancient cave", "enchanted forest"
    ]
}

LIGHTING = {
    "natural": [
        "soft morning light", "golden hour lighting", "sunset glow",
        "diffused natural light", "dawn forest light"
    ],
    "artificial": [
        "warm indoor lamp light", "neon city lights", "dim romantic candlelight",
        "studio softbox lighting", "cinematic blue hour light"
    ],
    "dramatic": [
        "dramatic shadows", "rim lighting", "volumetric lighting",
        "moody noir lighting", "god rays"
    ]
}

EXPRESSIONS = {
    "soft": [
        "soft smile", "gentle gaze", "shy look", "warm smile", "peaceful expression"
    ],
    "seductive": [
        "seductive smirk", "biting lip", "half-lidded eyes", "intense gaze", "looking up through lashes"
    ],
    "intense": [
        "flustered face", "heavy breathing", "parted lips", "rolling eyes", "tongue out"
    ],
    "pleasure": [
        "ahegao", "messy face", "eyes rolled back", "saliva trail", "ecstatic expression"
    ]
}

CAMERA_ANGLES = [
    "eye level shot", "low angle shot", "high angle shot", "dutch angle",
    "close up shot", "cowboy shot", "full body shot", "from below", "from above"
]

CAMERA_LENS = [
    "wide angle lens", "ultra wide angle lens", "telephoto lens", "85mm portrait lens", 
    "50mm prime lens", "35mm street lens", "100mm macro lens", "fisheye lens",
    "sharp depth of field"
]

MALE_INTERACTIONS = {
    "touch_breasts": [
        "strong male hands cupping both breasts from behind",
        "male hands squeezing breasts firmly",
        "male hands massaging breasts softly",
        "male hands lifting breasts from below"
    ],
    "body_contact": [
        "male arm around her waist pulling her close",
        "male hands gripping her hips",
        "male hands on her thighs"
    ]
}

FANTASY_RACES = {
    "werewolf": {
        "features": "werewolf humanoid with wolf ears and claws, golden eyes",
        "hands": "clawed hands",
        "description": "silver fur on shoulders and arms"
    },
    "dragon": {
        "features": "dragon humanoid with horns scales and tail, wings",
        "hands": "scaled hands",
        "description": "scales and wings visible"
    },
    "elf": {
        "features": "elf humanoid with pointed ears and glowing eyes",
        "hands": "elegant hands",
        "description": "ethereal glow"
    },
    "orc": {
        "features": "orc humanoid with green skin and tusks",
        "hands": "large rough hands",
        "description": "muscular green body"
    }
}

NEGATIVE_PROMPTS = {
    "sfw": "cleavage, low neckline, see-through, wet fabric, nipples, areola, underwear visible, sideboob, underboob, childlike, bangs, low quality, blurry, deformed, watermark, text",
    "tease": "visible nipples, areola, full nudity, childlike, bangs, low quality, blurry, deformed, watermark, text",
    "nsfw": "childlike, loli, underage, bangs, low quality, blurry, deformed, extra limbs, bad anatomy, watermark, text, logo, mirror reflection",
    "fantasy": "real animal, four legs, full fur body, childlike, bangs, low quality, blurry, deformed, watermark, text"
}

HASHTAGS = {
    "base": ["#Seoyeon", "#MorningRoutine", "#SoftAesthetic", "#SeoulVibes", "#GoldenHour", "#CozyVibes", "#PrivateMoments"],
    "sfw_add": ["#HotelLife"],
    "tease_add": ["#AfterHours", "#SilkGlow"]
}

CAPTIONS = {
    "sfw": [
        "Quiet mornings in Seoul…",
        "Just checked into the new suite. View is amazing! 🌆",
        "Coffee first, everything else second. ☕️",
        "Cozy vibes today.",
        "Simple days are the best days."
    ],
    "tease": [
        "Should I leave the door unlocked? 🚪",
        "It’s getting a bit warm in here…",
        "Just finished my shower. Feeling fresh.",
        "Thinking of you.",
        "Late night thoughts."
    ]
}

RACE_TRANSFORMATIONS = {
    "succubus": {
        "skin_change": "red skin",
        "special_features": "small horns, bat wings, tail, glowing red eyes, fangs",
        "hair_change": "crimson wavy hair",
        "body_change": None 
    },
    "snow_elf": {
        "skin_change": "pale blue skin",
        "special_features": "long pointed ears, frost patterns on skin, glowing blue eyes",
        "hair_change": "white hair",
        "body_change": None
    },
    "dark_elf": {
        "skin_change": "dark grey skin",
        "special_features": "long cleaning ears, red eyes, silver tattoos",
        "hair_change": "silver hair",
        "body_change": None
    },
    "demon": {
        "skin_change": "pale skin",
        "special_features": "curved ram horns, black sclera eyes, sharp claws",
        "hair_change": "black hair",
        "body_change": None
    },
    "mermaid": {
        "skin_change": None,
        "special_features": "iridescent scales below waist",
        "hair_change": "turquoise hair",
        "body_change": "scales below waist instead of legs"
    },
    "dark_angel": {
        "skin_change": None,
        "special_features": "black wings, halo, violet eyes",
        "hair_change": "purple hair",
        "body_change": None
    },
    "orc_female": {
        "skin_change": "green skin",
        "special_features": "small tusks, pointed ears, war paint",
        "hair_change": "black braided hair",
        "body_change": "muscular slim body"
    },
    "fairy": {
        "skin_change": None,
        "special_features": "glowing translucent wings, flower crown",
        "hair_change": "pastel pink hair",
        "body_change": None
    }
}

MASTURBATION_ACTIONS = {
    "hand_positions": {
        "one_hand_breast_one_hand_clit": {
            "breast_hand": "one hand squeezing {SIDE} breast",
            "lower_hand": "other hand rubbing clit",
            "description": "hands busy on body"
        },
        "both_hands_breasts": {
            "breast_hand": "both hands squeezing breasts together",
            "lower_hand": "",
            "description": "playing with breasts"
        },
        "fingering": {
            "hand_1": "one hand spreading labia",
            "hand_2": "other hand {FINGER_COUNT} fingers inserted",
            "advanced": "one hand spreading, other hand two fingers inside + thumb on clit"
        }
    },
    "body_positions": {
        "on_back": {
            "legs": ["spread wide", "in air", "bent"],
            "description": "lying on back"
        },
        "on_stomach": {
            "variations": ["ass up", "flat", "one leg raised"],
            "description": "lying on stomach"
        },
        "kneeling": {
            "variations": ["legs spread", "leaning forward"],
            "description": "kneeling"
        },
        "side": {
            "variations": ["one leg up"],
            "description": "lying sideways"
        },
        "standing": {
            "variations": ["one leg raised on furniture", "leaning against wall"],
            "description": "standing"
        }
    }
}

CLOTHING_EXPOSURE_STATES = {
    "lifted_top": "lifting shirt to reveal breasts",
    "pulled_down_bottom": "pulling down panties",
    "open_shirt": "shirt unbuttoned open",
    "skirt_lifted": "lifting skirt up"
}

PUBLIC_LOCATIONS = {
    "cafe_bathroom": {
        "desc": "cramped public bathroom stall",
        "risk": "steamy mirror"
    },
    "park_bench_night": {
        "desc": "dark park bench at night",
        "risk": "distant streetlights"
    },
    "fitting_room": {
        "desc": "clothing store fitting room",
        "risk": "mirror reflection"
    },
    "car_backseat": {
        "desc": "backseat of a parked car",
        "risk": "leather seats"
    }
}

PUBLIC_EXPRESSIONS = [
    "looking around nervously",
    "nervous pleasure expression",
    "nervous thrill expression",
    "trying to stay quiet",
    "biting lip to suppress sound"
]

# Translation Dictionary
K_TRANS = {
    "cafe window": "카페 창가", "hotel room": "호텔 방", "luxury lounge": "고급 라운지", "cozy armchair": "안락의자", "bedroom": "침실",
    "hotel lobby": "호텔 로비", "restaurant booth": "레스토랑 부스", "art gallery": "미술관", "penthouse suite": "펜트하우스",
    "rooftop terrace": "루프탑 테라스", "balcony": "발코니", "outdoor cafe table": "야외 카페", "rooftop pool": "루프탑 수영장",
    "empty late-night bus back seat": "심야 버스 뒷좌석", "empty subway car": "빈 지하철 객차", "private yacht deck": "요트 갑판",
    "forest cabin": "숲속 오두막", "spaceship interior": "우주선 내부", "ancient cave": "동굴", "enchanted forest": "마법의 숲",
    # Poses & Actions
    "sitting by cafe window": "카페 창가에 앉아", "sitting on couch": "소파에 앉아", "sitting at desk": "책상에 앉아",
    "sitting on bed": "침대에 앉아", "sitting at dinner table": "식탁에 앉아",
    "standing by window": "창가에 서서", "standing in lobby": "로비에 서서", "leaning against wall": "벽에 기대어",
    "standing by floor lamp": "조명 옆에 서서",
    "lying on back on bed": "침대에 누워", "lying on stomach on bed": "침대에 엎드려", "lying on fur rug": "러그 위에 누워",
    "hands holding coffee cup": "커피잔을 들고", "holding book": "책을 들고", "holding wine glass": "와인잔을 들고",
    "arms crossed": "팔짱을 끼고", "hand touching neck": "목에 손을 대고",
    # Expressions
    "gentle smile": "부드러운 미소", "soft smile": "은은한 미소", "seductive smirk": "유혹적인 미소", "intense gaze": "강렬한 눈빛"
}
