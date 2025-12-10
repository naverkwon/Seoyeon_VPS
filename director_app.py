import streamlit as st
import random
import time
import os
import director_data as dd
import director_lib as lib

# ==========================================
# UI Helpers
# ==========================================
def tx(key):
    lang_code = st.session_state.get("lang_code", "KR")
    return dd.TRANSLATIONS[lang_code].get(key, key)

# ==========================================
# Main App Layout
# ==========================================
st.set_page_config(page_title="Seoyeon VPS: Director Mode", page_icon="None", layout="wide")

# Load Custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Init Session State
keys = ["r_shot", "r_angle", "r_lens", "r_light", "r_hair", "r_face", "r_outfit_cat", "r_outfit", "r_loc", "r_makeup", "r_action", "history", "final_prompt_s", "storyboard_plan"]
defaults = [
    list(dd.SHOT_TYPES.keys())[1], # Shot
    dd.LOGIC_MAP[list(dd.SHOT_TYPES.keys())[1]]["angles"][0], # Angle
    dd.LOGIC_MAP[list(dd.SHOT_TYPES.keys())[1]]["default_lens"], # Lens
    list(dd.LIGHTING_DICT.keys())[0], # Light
    dd.HAIRSTYLES[0],
    dd.EXPRESSIONS[0], # Face/Expression
    list(dd.OUTFITS.keys())[0], dd.OUTFITS["Casual"][0], "", "", "", [], "", []
]
for k, d in zip(keys, defaults):
    if k not in st.session_state: st.session_state[k] = d

# --- LEFT COLUMN: MENU ---
with st.sidebar:
    st.header("VPS Control Center")
    
    # Global Config
    with st.expander("Settings", expanded=True):
        # Engine
        st.caption("Generation Engine")
        # Default index=1 (Cloud)
        engine = st.radio("Engine", [tx("engine_local"), tx("engine_cloud")], index=1, label_visibility="collapsed", key="engine_radio")
        st.session_state.engine = engine

        # Server Status
        if "Local" in tx("engine_local") and "Local" in engine or "로컬" in engine: # Cross-lang check
            if lib.check_server(): st.success("Local System Online")
            else: st.error("Local System Offline")
        else:
            if "REPLICATE_API_TOKEN" in os.environ: st.success("Cloud System Ready")
            else: st.error("Token Missing")

    # Mode Selection
    st.divider()
    mode = st.radio("Operation Mode", [tx("mode_single"), tx("mode_story")], index=0)

    # Turbo Mode (New)
    st.divider()
    turbo_mode = st.toggle("Turbo Mode", value=False, help="Skip preview and generate immediately")

    # Tools
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Open Folder"):
            lib.open_folder(os.path.join(os.getcwd(), "generated_images"))
    with c2:
        if st.button("Reload"):
            st.rerun()
            
    st.markdown("---")
    st.link_button("Go to Homepage Gallery", "http://localhost:5001/gallery", use_container_width=True)

# --- MAIN LAYOUT ---
# Header with Language Toggle on Right
h_col1, h_col2 = st.columns([6, 1])
with h_col1:
    st.title(tx("title"))
with h_col2:
    # Language Selector (Compact)
    lang_select = st.selectbox("Language", ["KR", "EN"], label_visibility="collapsed", key="lang_select_main")
    st.session_state.lang_code = "KR" if "KR" in lang_select else "EN"

# [MODE A] Single Shot
if mode == tx("mode_single"):
    
    # Layout: Split 60% (Controls) / 40% (Monitor)
    col_controls, col_monitor = st.columns([1.5, 1], gap="large")

    # === LEFT: CONTROLS ===
    with col_controls:
        # [1] Action & Context (Reordered: Was [3])
        with st.container(border=True):
            st.subheader(tx("header_action"))
            
            # Action AI
            a1, a2 = st.columns([3, 1])
            action_desc = a1.text_area(tx("label_action"), height=80, key="r_action", placeholder="e.g. Drinking coffee")
            
            def generate_ai_action_callback():
                st.session_state.r_action = lib.generate_ai_action()

            if a2.button("Auto", help="Generate AI Action", use_container_width=True, on_click=generate_ai_action_callback):
                 pass
            
            location_desc = st.text_input(tx("label_location"), value=st.session_state.r_loc, key="r_loc")

        # [2] Styling (Unchanged position, but conceptually 2nd)
        with st.container(border=True):
            st.subheader(tx("header_style"))
            
            s1, s2 = st.columns(2)
            hair = s1.selectbox(tx("label_hair"), dd.HAIRSTYLES, key="r_hair")
            
            # Smart Active Logic
            # Note: shot_type variable is needed here, so we must defer logic or init it early.
            # However, since shot_type is in Camera block (now [3]), we have a dependency issue.
            # Fix: We lift the shot_type SELECTOR to valid scope or default it. 
            # Better UI Flow: The user sets Action -> Style -> Camera. 
            # Valid angles/lenses depend on shot type, but style constraints (shoes etc) also depend on shot type.
            # To fix dependency without massive refactor: Initialize defaults at top of loop or handle gracefully.
            
            # Temporary fix: Get shot_type from session_state if available, else default
            current_shot = st.session_state.get("r_shot", list(dd.SHOT_TYPES.keys())[0])
            
            is_close = "클로즈업" in current_shot or "Close-up" in current_shot
            is_full = "전신" in current_shot or "Full Body" in current_shot
            
            # Expression & Makeup
            f1, f2 = st.columns(2)
            face_exp = f1.selectbox(tx("label_expression"), dd.EXPRESSIONS, key="r_face")
            makeup = f2.text_input(tx("label_makeup"), placeholder="e.g. Red Lips", key="r_makeup")

            st.divider()
            
            # Outfit System
            o1, o2 = st.columns([1.2, 2])
            outfit_cat = o1.selectbox(tx("label_outfit_cat"), list(dd.OUTFITS.keys()), key="r_outfit_cat")
            
            avail_outfits = dd.OUTFITS[outfit_cat] + ["(Custom)"]
            
            # Sync Logic for Outfit Index
            current_out = st.session_state.r_outfit
            o_idx = 0
            if current_out in avail_outfits: o_idx = avail_outfits.index(current_out)
            
            outfit_select = o2.selectbox(tx("label_outfit"), avail_outfits, index=o_idx, key="r_outfit")
            
            # Outfit value lookup
            outfit_val = outfit_select
            if outfit_select == "(Custom)":
                outfit_val = st.text_input("Custom Outfit", placeholder=tx("placeholder_outfit"))
            
            # Accessories (Smart Context)
            if is_full: acc_text = st.text_input(tx("label_acc_full"), placeholder="Heels/Stockings/Shoes", key="r_acc_full")
            elif is_close: acc_text = st.text_input(tx("label_acc_close"), placeholder="Earrings/Necklace", key="r_acc_close")
            else: acc_text = st.text_input(tx("label_acc_gen"), key="r_acc_gen")

        # [3] Camera Logic (Reordered: Was [1])
        with st.container(border=True):
            c_head, c_rand = st.columns([4, 1])
            c_head.subheader(tx("header_camera"))
            # Random Logic Simplified inline
            if c_rand.button("Random", help=tx("btn_random")):
                shot = random.choice(list(dd.SHOT_TYPES.keys()))
                st.session_state.r_shot = shot
                logic = dd.LOGIC_MAP[shot]
                st.session_state.r_angle = random.choice(logic["angles"])
                st.session_state.r_lens = random.choice(logic["lens"])
                st.rerun()

            # Shot & Lens
            c1, c2 = st.columns(2)
            shot_type = c1.selectbox(tx("label_shot"), list(dd.SHOT_TYPES.keys()), key="r_shot")
            
            # Logic Filter
            valid_angles = dd.LOGIC_MAP[shot_type]["angles"]
            valid_lenses = dd.LOGIC_MAP[shot_type]["lens"]
            
            # Auto-correction
            if st.session_state.r_angle not in valid_angles: st.session_state.r_angle = valid_angles[0]
            if st.session_state.r_lens not in valid_lenses: st.session_state.r_lens = valid_lenses[0]

            lens = c2.selectbox(tx("label_lens"), valid_lenses, key="r_lens")
            
            # Angle & Light
            c3, c4 = st.columns(2)
            angle = c3.selectbox(tx("label_angle"), valid_angles, key="r_angle")
            lighting = c4.selectbox(tx("label_light"), list(dd.LIGHTING_DICT.keys()), key="r_light")

        # [4] Generate Action (Turbo vs Normal)
        st.divider()
        
        # Prepare Prompt Data (UPDATED STRUCTURE)
        def build_prompt():
            
            # 1. FIXED QUALITY & SUBJECT
            p_quality = dd.PROMPT_QUALITY
            p_subject = dd.PROMPT_SUBJECT
            p_body = dd.PROMPT_BODY
            
            # 2. HAIR (Base + Style)
            t_hair_style = dd.HAIRSTYLES_DICT.get(hair, hair)
            p_hair = f"{dd.PROMPT_HAIR_BASE}, {t_hair_style}"
            
            # NEW: FACE & MAKEUP
            t_exp = dd.EXPRESSIONS_DICT.get(face_exp, "")
            t_makeup = lib.translate_to_eng(makeup)
            if not t_makeup: t_makeup = "natural minimal makeup" # Default if empty
            
            p_face = f"{p_subject}, {t_exp}, {t_makeup}"

            # 3. OUTFIT / ACC
            if outfit_select == "(Custom)":
                t_outfit = lib.translate_to_eng(outfit_val)
            else:
                 t_outfit = dd.OUTFITS_DICT.get(outfit_cat, {}).get(outfit_select, outfit_val)

            t_acc = lib.translate_to_eng(acc_text)
            
            # 4. ACTION / LOCATION / TECHNICAL
            t_action = lib.translate_to_eng(action_desc)
            t_loc = lib.translate_to_eng(location_desc)
            
            t_shot = dd.SHOT_TYPES[shot_type]
            t_angle = dd.ANGLES_DICT[angle]
            t_lens = dd.LENS_DICT[lens]
            t_light = dd.LIGHTING_DICT[lighting]

            # ASSEMBLY ORDER: 
            # Quality -> Subject(Face+Exp+Makeup) -> Hair -> Body -> Outfit -> Action -> Env -> Tech
            parts = [
                p_quality,
                t_shot, 
                t_angle,
                t_lens,
                p_face, # Updated Subject block
                p_hair,
                p_body,
                f"{t_outfit}" if t_outfit else "", 
                t_acc,
                t_action,
                t_loc,
                f"{t_light}, film grain"
            ]
            return ", ".join([p for p in parts if p])

        if turbo_mode:
            # TURBO: One-Click Shoot
            if st.button("SHOOT (Turbo)", type="primary", use_container_width=True):
                final_prompt = build_prompt()
                st.session_state.final_prompt_s = final_prompt
                
                with st.status(f"Turbo Generating ({engine})...", expanded=True):
                    seed = random.randint(0, 10**14)
                    try:
                        img = lib.generate_image(engine, final_prompt, seed)
                        if img:
                            fpath = lib.save_image_to_disk(img, final_prompt)
                            caption = lib.generate_caption(final_prompt)
                            lib.save_metadata(fpath, final_prompt, seed, caption)
                            st.toast(f"Caption: {caption}")
                            st.session_state.history.insert(0, {"img": img, "seed": seed, "prompt": final_prompt, "time": time.strftime("%H:%M:%S"), "engine": engine, "caption": caption})
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

        else:
            # NORMAL: Preview -> Shoot
            if st.button(tx("btn_preview"), use_container_width=True):
                st.session_state.final_prompt_s = build_prompt()
            
            if st.session_state.final_prompt_s:
                st.info("Ready to Shoot")

    # === RIGHT: MONITOR ===
    with col_monitor:
        # Gallery Tab System
        tab_preview, tab_history, tab_logs = st.tabs(["Preview", "History", "Logs"])
        
        with tab_preview:
            if st.session_state.history:
                last_item = st.session_state.history[0]
                st.image(last_item['img'], caption=f"Last Shot ({last_item['time']})", use_container_width=True)
                if last_item.get('caption'):
                    st.success(last_item['caption'])
            else:
                st.empty()
                st.container(height=300, border=True).markdown("### 📡 No Signal\n\nGenerate an image to see it here.")

            # Preview Text Source (if not Turbo)
            if not turbo_mode and st.session_state.final_prompt_s:
                # 1. Negative Prompt Display (Global)
                with st.expander(tx("label_neg"), expanded=False):
                    st.code(dd.NEGATIVE_PROMPT, language="text")

                # 2. Positive Prompt Display
                st.caption("📝 Positive Prompt")
                st.info(st.session_state.final_prompt_s, icon="📝")
                
                st.divider()
                st.caption("📋 Copy Data")
                
                # Positive
                st.markdown("**Positive:**")
                st.code(st.session_state.final_prompt_s, language="text")
                
                # Negative
                st.markdown("**⛔ Negative:**")
                st.code(dd.NEGATIVE_PROMPT, language="text")
        
        # Shoot Button Implementation for Normal Mode (placed in Monitor for flow)
        if not turbo_mode and st.session_state.final_prompt_s:
             if tab_preview.button("SNAP SHUTTER", type="primary", use_container_width=True):
                    with st.status(f"{engine} Shooting...", expanded=True) as status:
                        seed = random.randint(0, 10**14)
                        try:
                            img = lib.generate_image(engine, st.session_state.final_prompt_s, seed)
                            if img:
                                fpath = lib.save_image_to_disk(img, st.session_state.final_prompt_s)
                                caption = lib.generate_caption(st.session_state.final_prompt_s)
                                lib.save_metadata(fpath, st.session_state.final_prompt_s, seed, caption)
                                st.toast(f"Caption: {caption}")
                                st.session_state.history.insert(0, {"img": img, "seed": seed, "prompt": st.session_state.final_prompt_s, "time": time.strftime("%H:%M:%S"), "engine": engine, "caption": caption})
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

        with tab_history:
            for item in st.session_state.history:
                st.image(item['img'], caption=item['time'])
        
        with tab_logs:
            for item in st.session_state.history:
                with st.expander(item['time']):
                    st.code(item['prompt'])

# [MODE B] Storyboard
elif mode == tx("mode_story") or mode.startswith("🎞️"):
    st.subheader(tx("mode_story"))
    c1, c2 = st.columns([1, 2], gap="large")
    
    with c1:
        with st.container(border=True):
            st.caption(tx("header_planning"))
            
            # Theme Section with Random Button
            # Theme Section
            c_t1, c_t2 = st.columns([3, 1], gap="small")
            with c_t1:
                st.markdown(f"**{tx('label_theme')}**")
            with c_t2:
                # Random Theme Button - Improved Layout
                if st.button("🎲 Random", use_container_width=True, help="Generate a random scenario"):
                     st.session_state.sb_th = lib.generate_random_theme()

            theme = st.text_area(tx("label_theme"), placeholder="e.g. Summer Vacation", key="sb_th", label_visibility="collapsed")
            plat = st.selectbox(tx("label_platform"), ["Instagram", "Patreon"], key="sb_pl")

            count = st.slider(tx("label_shots"), 3, 12, 6, key="sb_cnt")
            
            # Feature: Consistent Style
            consistent_style = st.checkbox("🧩 Consistent Style (Same Seed)", value=False, help="Use the same random seed for all shots to keep lighting/face consistent.")
            
            if st.button(tx("btn_generate_plan"), type="primary", use_container_width=True):
                if not lib.GEMINI_API_KEY:
                    st.error("Gemini API Key Missing")
                else:
                    with st.status(tx("status_thinking")):
                        st.session_state.storyboard_plan = lib.generate_storyboard(theme, plat, count)
                        if st.session_state.storyboard_plan: st.success("Completed!")
    
    with c2:
        if st.session_state.storyboard_plan:
            st.caption(tx("header_cue_sheet"))
            final_plan_prompts = []
            
            for i, s in enumerate(st.session_state.storyboard_plan):
                with st.expander(f"#{i+1} {s.get('title','Untitled')}", expanded=True):
                    cols = st.columns([3, 1])
                    pt = cols[0].text_area("Visual Prompt", s.get('visual_prompt',''), height=70, key=f"sp_{i}")
                    
                    # Logic: Map 'shot_type' to Index
                    rec_type = s.get('shot_type', 'Close-up')
                    st_keys = list(dd.SHOT_TYPES.keys())
                    st_idx = 0
                    if "Full" in rec_type: st_idx = 3 # 전신
                    elif "Cowboy" in rec_type or "Thigh" in rec_type: st_idx = 2 # 허벅지
                    elif "Upper" in rec_type: st_idx = 1 # 상반신
                    
                    ps = cols[1].selectbox("Shot Code", st_keys, index=st_idx, key=f"ss_{i}")
                    
                    # Logic Assembly (Batch)
                    log = dd.LOGIC_MAP[ps]
                    def_angle = log["angles"][0]
                    def_lens = log["default_lens"]
                    
                    l1 = dd.PROMPT_QUALITY # Use shared constant
                    l2 = dd.SHOT_TYPES[ps]
                    l3 = dd.ANGLES_DICT[def_angle]
                    l_lens = dd.LENS_DICT[def_lens]
                    
                    final_p = f"{l1}, {l2}, {l3}, {l_lens}, {dd.PROMPT_SUBJECT}, {pt}, {dd.PROMPT_BODY}" # Approximate structure for storyboard
                    final_plan_prompts.append(final_p)
            
            st.divider()
            
            if st.button(f"Start Batch Shooting ({len(final_plan_prompts)} Cuts)", type="primary", use_container_width=True):
                # Batch Execution
                progress_bar = st.progress(0)
                status_text = st.empty()
                result_images = []
                
                # Seed Logic
                base_seed = random.randint(0, 10**14)
                
                for idx, p_str in enumerate(final_plan_prompts):
                    status_text.write(f"Shooting Cut #{idx+1}...")
                    try:
                        # Use base_seed if consistent, else random
                        if consistent_style:
                            seed = base_seed
                        else:
                            seed = random.randint(0, 10**14)
                            
                        img = lib.generate_image(engine, p_str, seed)
                        
                        if img:
                            fpath = lib.save_image_to_disk(img, p_str)
                            caption = lib.generate_caption(p_str)
                            lib.save_metadata(fpath, p_str, seed, caption)
                            st.toast(f"Saved: {caption}")
                            
                            st.session_state.history.insert(0, {"img": img, "seed": seed, "prompt": p_str, "time": time.strftime("%H:%M:%S"), "engine": "Batch"})
                            result_images.append(img)
                            
                    except Exception as e:
                        st.error(f"Error on Cut #{idx+1}: {e}")
                    
                    progress_bar.progress((idx + 1) / len(final_plan_prompts))
                
                status_text.success("All Cuts Completed!")
                st.image(result_images, caption=[f"Cut #{x+1}" for x in range(len(result_images))])
