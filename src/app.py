"""Streamlit Web Application for Dune: Adventures in the Imperium Character Generator."""

import base64
import sys
from pathlib import Path

# Ensure src is in sys.path
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

import streamlit as st
import random
from dune_char_gen.models.character import Character, FocusItem, TalentItem, AssetItem
from dune_char_gen.models.enums import SkillName, DriveName, FactionType, AssetType, CharacterType
from dune_char_gen.models.validation import validate_character
from dune_char_gen.data.archetypes import ARCHETYPES, get_archetype, get_all_archetype_names
from dune_char_gen.data.factions import FACTION_TEMPLATES, get_faction_template
from dune_char_gen.data.skills_and_focuses import STANDARD_FOCUSES, SKILL_DESCRIPTIONS, get_all_focuses
from dune_char_gen.data.talents import TALENTS, get_talents_for_faction, get_talent
from dune_char_gen.data.drives import DRIVE_DESCRIPTIONS, DRIVE_STATEMENTS, AMBITION_EXAMPLES
from dune_char_gen.data.assets import ASSETS, get_all_asset_names
from dune_char_gen.data.houses import CANON_HOUSES, HOMEWORLDS, HOUSE_ROLES, PERSONAL_TRAITS
from dune_char_gen.data.names import generate_dune_name
from dune_char_gen.generators.random_generator import generate_random_character
from dune_char_gen.generators.npc_generator import generate_minor_npc, generate_notable_npc
from dune_char_gen.exporters.json_exporter import character_to_json, character_from_json
from dune_char_gen.exporters.markdown_exporter import character_to_markdown
from dune_char_gen.exporters.html_exporter import character_to_html

# Asset paths & Base64 encoders
assets_dir = Path(__file__).resolve().parent.parent / "assets"
icon_path = assets_dir / "icon.jpg"
bg_path = assets_dir / "background.jpg"

icon_b64 = ""
if icon_path.exists():
    with open(icon_path, "rb") as f:
        icon_b64 = base64.b64encode(f.read()).decode("utf-8")

bg_b64 = ""
if bg_path.exists():
    with open(bg_path, "rb") as f:
        bg_b64 = base64.b64encode(f.read()).decode("utf-8")

# Set page configuration
st.set_page_config(
    page_title="Dune: Adventures in the Imperium - Character Generator",
    page_icon=str(icon_path) if icon_path.exists() else "⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Dune-themed styling with background and typography
bg_css = f"""
    background-image: 
        linear-gradient(rgba(252, 249, 242, 0.88), rgba(252, 249, 242, 0.92)),
        url('data:image/jpeg;base64,{bg_b64}');
    background-attachment: fixed;
    background-position: center center;
    background-size: cover;
    background-repeat: no-repeat;
""" if bg_b64 else ""

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Fauna+One&display=swap');
    
    .stApp {{
        background-color: #fcf9f2;
        {bg_css}
        color: #2b2825;
    }}
    
    h1, h2, h3 {{
        font-family: 'Cinzel', serif !important;
        color: #8b4513 !important;
        letter-spacing: 1px;
    }}
    
    .dune-header {{
        background: linear-gradient(135deg, #1b1c1e 0%, #3a2e22 100%);
        color: #f7e8aa;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 14px;
        border-bottom: 2.5px solid #c88a38;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 16px;
    }}
    
    .dune-header h1 {{
        color: #e5b95c !important;
        margin: 0;
        font-size: 1.5rem;
    }}
    
    .dune-header p {{
        color: #d1c5b4;
        margin: 2px 0 0 0;
        font-size: 0.85rem;
        font-style: italic;
    }}
    
    .stat-card {{
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(4px);
        border: 1px solid #dcd2bf;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }}
    
    .badge-pill {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        background: #eee6d8;
        color: #5c4328;
        border: 1px solid #c88a38;
        margin-right: 6px;
    }}
    
    .validation-pass {{
        color: #2e7d32;
        font-weight: bold;
    }}
    
    .validation-fail {{
        color: #c62828;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "character" not in st.session_state:
    st.session_state["character"] = generate_random_character()

char: Character = st.session_state["character"]

# Header banner with App Icon
header_icon_html = f'<img src="data:image/jpeg;base64,{icon_b64}" style="width: 48px; height: 48px; border-radius: 50%; border: 2px solid #c88a38; box-shadow: 0 0 10px rgba(200, 138, 56, 0.45); object-fit: cover; flex-shrink: 0;">' if icon_b64 else ''

st.markdown(f"""
<div class="dune-header">
    {header_icon_html}
    <div>
        <h1>DUNE: ADVENTURES IN THE IMPERIUM</h1>
        <p>2d20 Roleplaying Game — Character Generator & Sheet Manager</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
if icon_b64:
    st.sidebar.markdown(f"""
    <div style="text-align: center; margin-bottom: 12px;">
        <img src="data:image/jpeg;base64,{icon_b64}" style="width: 80px; height: 80px; border-radius: 50%; border: 2.5px solid #c88a38; box-shadow: 0 2px 10px rgba(0,0,0,0.2); object-fit: cover;">
    </div>
    """, unsafe_allow_html=True)

st.sidebar.title("Navigation & Tools")
mode = st.sidebar.radio(
    "Mode",
    [
        "🧙 Character Creator Wizard",
        "🎲 Instant Random Character",
        "👥 Supporting NPC Generator",
        "📂 Character Vault & Export",
        "ℹ️ About & Credits",
    ],
    index=0,
)

# Rule validation status in sidebar
report = validate_character(char)
with st.sidebar.expander("⚖️ Rulebook Compliance Audit", expanded=True):
    if report.is_valid:
        st.markdown('<p class="validation-pass">✓ 100% Rulebook Compliant</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="validation-fail">✗ Has Validation Issues</p>', unsafe_allow_html=True)

    for check, passed in report.checks.items():
        icon = "✅" if passed else "❌"
        st.write(f"{icon} {check}")

    if report.errors:
        st.error("\n".join([f"• {e}" for e in report.errors]))
    if report.warnings:
        st.warning("\n".join([f"• {w}" for w in report.warnings]))

# Top Rule Audit Bar (Always visible on page load)
skill_sum = sum(char.skills.values())
focus_cnt = len(char.focuses)
talent_cnt = len(char.talents)
asset_cnt = len(char.assets)
status_badge = '<span class="validation-pass">✓ 100% Rulebook Compliant</span>' if report.is_valid else f'<span class="validation-fail">✗ {len(report.errors)} Rule Issue(s) Detected</span>'

st.markdown(f"""
<div style="background: #faf6ef; border: 1px solid #e2d4c0; border-left: 4px solid #c88a38; border-radius: 6px; padding: 7px 14px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; font-size: 0.85rem;">
    <div><strong>⚖️ Rules Audit:</strong> {status_badge}</div>
    <div style="color: #5c4328; font-size: 0.82rem;">
        <strong>Skills:</strong> {skill_sum}/28 &nbsp;|&nbsp;
        <strong>Focuses:</strong> {focus_cnt}/4 &nbsp;|&nbsp;
        <strong>Talents:</strong> {talent_cnt}/3 &nbsp;|&nbsp;
        <strong>Assets:</strong> {asset_cnt}/3
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# MODE 1: CHARACTER CREATOR WIZARD
# -------------------------------------------------------------
if mode == "🧙 Character Creator Wizard":
    tabs = st.tabs([
        "1. Concept & Faction",
        "2. Archetype",
        "3. Skills & Focuses",
        "4. Talents",
        "5. Drives & Statements",
        "6. Assets",
        "7. Ambition & Details",
        "8. Character Sheet Preview",
    ])

    # TAB 1: CONCEPT & FACTION
    with tabs[0]:
        st.subheader("Step 1: Concept & Allegiance")
        col1, col2 = st.columns([2, 1])

        with col1:
            col_n1, col_n2 = st.columns([3, 1])
            with col_n1:
                char.name = st.text_input("Character Name", value=char.name)
            with col_n2:
                st.write("")
                st.write("")
                if st.button("🎲 Suggest Name"):
                    char.name = generate_dune_name(char.faction)
                    st.rerun()

            char.concept = st.text_input("Character Concept Summary", value=char.concept,
                                         help="E.g., Cunning spymaster serving House Atreides or Fremen sandrider guide.")

            col_h1, col_h2 = st.columns(2)
            with col_h1:
                house_list = CANON_HOUSES + (["Custom House"] if char.house not in CANON_HOUSES else [])
                house_idx = house_list.index(char.house) if char.house in house_list else 0
                selected_house = st.selectbox("House Allegiance", house_list, index=house_idx)
                if selected_house == "Custom House":
                    char.house = st.text_input("Custom House Name", value=char.house)
                else:
                    char.house = selected_house

            with col_h2:
                hw_list = HOMEWORLDS + (["Custom World"] if char.homeworld not in HOMEWORLDS else [])
                hw_idx = hw_list.index(char.homeworld) if char.homeworld in hw_list else 0
                selected_hw = st.selectbox("Homeworld", hw_list, index=hw_idx)
                if selected_hw == "Custom World":
                    char.homeworld = st.text_input("Custom Homeworld Name", value=char.homeworld)
                else:
                    char.homeworld = selected_hw

            col_r1, col_r2 = st.columns(2)
            with col_r1:
                role_list = HOUSE_ROLES + (["Custom Role"] if char.house_role not in HOUSE_ROLES else [])
                r_idx = role_list.index(char.house_role) if char.house_role in role_list else 0
                selected_role = st.selectbox("Role in the House", role_list, index=r_idx)
                if selected_role == "Custom Role":
                    char.house_role = st.text_input("Custom Role Name", value=char.house_role)
                else:
                    char.house_role = selected_role

            with col_r2:
                trait_list = PERSONAL_TRAITS + (["Custom Trait"] if char.personal_trait not in PERSONAL_TRAITS else [])
                p_idx = trait_list.index(char.personal_trait) if char.personal_trait in trait_list else 0
                selected_trait = st.selectbox("Personal Trait", trait_list, index=p_idx)
                if selected_trait == "Custom Trait":
                    char.personal_trait = st.text_input("Custom Trait Name", value=char.personal_trait)
                else:
                    char.personal_trait = selected_trait

        with col2:
            st.markdown("### Faction Template")
            faction_options = list(FactionType)
            f_idx = faction_options.index(char.faction)
            chosen_faction = st.selectbox(
                "Faction Affiliation",
                faction_options,
                index=f_idx,
                format_func=lambda x: x.value
            )
            char.faction = chosen_faction
            fac_info = get_faction_template(chosen_faction)
            char.faction_trait = fac_info.additional_trait

            st.info(fac_info.description)
            if fac_info.additional_trait:
                st.write(f"**Bonus Trait:** `{fac_info.additional_trait}`")
            if fac_info.mandatory_talents:
                req_text = "ALL mandatory talents required" if fac_info.require_all_mandatory else "Pick at least ONE"
                st.write(f"**Mandatory Talent(s) ({req_text}):**")
                for mt in fac_info.mandatory_talents:
                    st.write(f"- `{mt}`")

    # TAB 2: ARCHETYPE
    with tabs[1]:
        st.subheader("Step 2: Choose Archetype")
        arch_names = get_all_archetype_names()
        curr_arch_idx = arch_names.index(char.archetype) if char.archetype in arch_names else 0
        selected_arch_name = st.selectbox("Select Archetype", arch_names, index=curr_arch_idx)
        
        if selected_arch_name != char.archetype:
            char.archetype = selected_arch_name
            char.archetype_trait = selected_arch_name

        arch_data = get_archetype(char.archetype)
        if arch_data:
            col_a1, col_a2 = st.columns([1, 1])
            with col_a1:
                st.markdown(f"#### {arch_data.name}")
                st.write(arch_data.description)
                st.markdown(f"**Archetype Trait:** `{char.archetype_trait}`")
                st.markdown(f"**Primary Skill:** :red[**{arch_data.primary_skill.value}**] (Starts at 6)")
                st.markdown(f"**Secondary Skill:** :blue[**{arch_data.secondary_skill.value}**] (Starts at 5)")
                st.markdown(f"**Other Skills:** 4")
            with col_a2:
                st.markdown("#### Suggestions")
                st.write(f"**Suggested Focuses:** {', '.join(arch_data.suggested_focuses)}")
                st.write(f"**Suggested Talent:** `{arch_data.suggested_talent}`")
                st.write(f"**Drive Philosophy:** *{arch_data.drive_advice}*")

    # TAB 3: SKILLS & FOCUSES
    with tabs[2]:
        st.subheader("Step 3 & 4: Skills & Focuses")
        arch_data = get_archetype(char.archetype)
        
        # Skill points counter
        total_pts = sum(char.skills.values())
        rem_pts = 28 - total_pts
        if rem_pts == 0:
            st.success(f"Skill Points: **{total_pts}/28** (Allocation complete!)")
        elif rem_pts > 0:
            st.warning(f"Skill Points: **{total_pts}/28** ({rem_pts} points remaining to distribute).")
        else:
            st.error(f"Skill Points: **{total_pts}/28** (Over budget by {-rem_pts} points!).")

        st.caption("Base: Primary=6, Secondary=5, Others=4. Distribute 5 points across skills (min 4, max 8).")

        col_sk, col_fc = st.columns([1, 1])
        with col_sk:
            st.markdown("### Skill Ratings")
            for sk in SkillName:
                is_pri = arch_data and arch_data.primary_skill == sk
                is_sec = arch_data and arch_data.secondary_skill == sk
                label_tag = " (Primary)" if is_pri else (" (Secondary)" if is_sec else "")
                
                val = st.number_input(
                    f"{sk.value}{label_tag}",
                    min_value=4,
                    max_value=8,
                    value=char.get_skill(sk),
                    key=f"sk_{sk.value}",
                    help=SKILL_DESCRIPTIONS.get(sk, "")
                )
                char.set_skill(sk, val)

        with col_fc:
            st.markdown("### Focuses (Choose 4)")
            if arch_data:
                st.caption(f"Rule: At least 1 focus must be assigned to your primary skill ({arch_data.primary_skill.value}).")

            # Ensure we have 4 focus slots
            while len(char.focuses) < 4:
                char.focuses.append(FocusItem(name="General", skill=arch_data.primary_skill if arch_data else SkillName.BATTLE))

            for i in range(4):
                f_item = char.focuses[i]
                c1, c2 = st.columns([1, 2])
                with c1:
                    sk_options = list(SkillName)
                    sk_idx = sk_options.index(f_item.skill) if f_item.skill in sk_options else 0
                    new_sk = st.selectbox(f"Skill #{i+1}", sk_options, index=sk_idx, key=f"f_sk_{i}", format_func=lambda x: x.value)
                    f_item.skill = new_sk
                with c2:
                    std_list = STANDARD_FOCUSES.get(new_sk, [])
                    curr_val = f_item.name
                    # Let user pick from standard list or type custom
                    f_options = std_list + (["Custom Focus..."] if curr_val not in std_list else ["Custom Focus..."])
                    f_idx = f_options.index(curr_val) if curr_val in f_options else len(f_options) - 1
                    picked = st.selectbox(f"Focus #{i+1}", f_options, index=f_idx, key=f"f_name_sel_{i}")
                    if picked == "Custom Focus...":
                        custom_focus = st.text_input(f"Enter Custom Focus #{i+1}", value=curr_val if curr_val != "Custom Focus..." else "", key=f"f_cust_{i}")
                        f_item.name = custom_focus if custom_focus else "Specialty"
                    else:
                        f_item.name = picked

    # TAB 4: TALENTS
    with tabs[3]:
        st.subheader("Step 5: Talents (Select 3)")
        fac_template = get_faction_template(char.faction)
        available_talents = get_talents_for_faction(char.faction.value if char.faction != FactionType.NONE else None)
        avail_names = [t.name for t in available_talents]

        if fac_template.mandatory_talents:
            req_note = "ALL mandatory talents" if fac_template.require_all_mandatory else "at least ONE mandatory talent"
            st.info(f"**Faction Requirement:** As a {fac_template.name}, you must take {req_note} from: {', '.join(fac_template.mandatory_talents)}.")

        while len(char.talents) < 3:
            char.talents.append(TalentItem(name=avail_names[0] if avail_names else "Bold"))

        for i in range(3):
            t_item = char.talents[i]
            st.markdown(f"#### Talent #{i+1}")
            c_t1, c_t2 = st.columns([1, 2])
            with c_t1:
                t_options = avail_names + (["Custom Talent..."] if t_item.name not in avail_names else ["Custom Talent..."])
                t_idx = t_options.index(t_item.name) if t_item.name in t_options else 0
                picked_t = st.selectbox(f"Select Talent #{i+1}", t_options, index=t_idx, key=f"t_sel_{i}")
                
                if picked_t == "Custom Talent...":
                    t_name_custom = st.text_input(f"Custom Talent Name #{i+1}", value=t_item.name, key=f"t_cust_{i}")
                    t_item.name = t_name_custom
                else:
                    t_item.name = picked_t
                    t_def = get_talent(picked_t)
                    if t_def:
                        t_item.description = t_def.rules

                # Check if talent takes a specialization (like Skill or Drive)
                t_def = get_talent(t_item.name)
                if t_def and t_def.skill_param:
                    spec = st.selectbox(f"Skill for {t_item.name}", [s.value for s in SkillName], key=f"t_spec_{i}")
                    t_item.specialization = spec
                elif t_def and t_def.drive_param:
                    spec = st.selectbox(f"Drive for {t_item.name}", [d.value for d in DriveName], key=f"t_spec_{i}")
                    t_item.specialization = spec
                else:
                    t_item.specialization = None

            with c_t2:
                t_def = get_talent(t_item.name)
                if t_def:
                    st.markdown(f"*{t_def.flavor}*")
                    st.write(t_def.rules)
                    if t_def.faction_requirement:
                        st.caption(f"Faction Requirement: {t_def.faction_requirement}")
                else:
                    custom_desc = st.text_area(f"Talent #{i+1} Description", value=t_item.description, key=f"t_desc_{i}")
                    t_item.description = custom_desc
            st.markdown("---")

    # TAB 5: DRIVES & STATEMENTS
    with tabs[4]:
        st.subheader("Step 6: Drives & Drive Statements")
        st.caption("Assign the ratings 8, 7, 6, 5, and 4 among your five drives. Provide a statement for the 3 highest drives (8, 7, 6).")

        col_dr, col_st = st.columns([1, 2])
        with col_dr:
            st.markdown("### Drive Scores")
            for d in DriveName:
                d_val = st.selectbox(
                    f"{d.value}",
                    [8, 7, 6, 5, 4],
                    index=[8, 7, 6, 5, 4].index(char.get_drive(d)),
                    key=f"drv_{d.value}",
                    help=DRIVE_DESCRIPTIONS.get(d, "")
                )
                char.set_drive(d, d_val)

            # Check uniqueness
            vals = list(char.drives.values())
            if sorted(vals) != [4, 5, 6, 7, 8]:
                st.error("Each rating (8, 7, 6, 5, 4) must be assigned to exactly ONE drive!")
            else:
                st.success("Drives ratings correctly distributed.")

        with col_st:
            st.markdown("### Drive Statements (for scores 8, 7, 6)")
            top_drives = [d for d, val in char.drives.items() if val >= 6]
            # Sort descending
            top_drives = sorted(top_drives, key=lambda x: char.get_drive(x), reverse=True)

            for d in top_drives:
                st.markdown(f"**{d.value} (Rating: {char.get_drive(d)})**")
                curr_stmt = char.drive_statements.get(d, "")
                options = DRIVE_STATEMENTS.get(d, []) + (["Custom Statement..."] if curr_stmt not in DRIVE_STATEMENTS.get(d, []) else ["Custom Statement..."])
                s_idx = options.index(curr_stmt) if curr_stmt in options else len(options) - 1
                picked_s = st.selectbox(f"Statement for {d.value}", options, index=s_idx, key=f"stmt_sel_{d.value}")
                
                if picked_s == "Custom Statement...":
                    custom_stmt = st.text_input(f"Enter Custom {d.value} Statement", value=curr_stmt if curr_stmt != "Custom Statement..." else "", key=f"stmt_cust_{d.value}")
                    char.drive_statements[d] = custom_stmt
                else:
                    char.drive_statements[d] = picked_s

    # TAB 6: ASSETS
    with tabs[5]:
        st.subheader("Step 7: Starting Assets (Choose 3)")
        st.caption("You start with 3 assets, at least one of which must be Tangible.")

        all_asset_names = get_all_asset_names()

        while len(char.assets) < 3:
            char.assets.append(AssetItem(name="Kindjal", asset_type=AssetType.TANGIBLE))

        for i in range(3):
            st.markdown(f"#### Asset #{i+1}")
            a_item = char.assets[i]
            c_a1, c_a2 = st.columns([1, 2])
            with c_a1:
                options = all_asset_names + (["Custom Asset..."] if a_item.name not in all_asset_names else ["Custom Asset..."])
                a_idx = options.index(a_item.name) if a_item.name in options else 0
                picked_a = st.selectbox(f"Asset #{i+1}", options, index=a_idx, key=f"a_sel_{i}")
                
                if picked_a == "Custom Asset...":
                    a_custom_name = st.text_input(f"Custom Asset #{i+1} Name", value=a_item.name, key=f"a_cust_name_{i}")
                    a_item.name = a_custom_name
                    a_type = st.selectbox(f"Type #{i+1}", [AssetType.TANGIBLE, AssetType.INTANGIBLE], key=f"a_type_{i}", format_func=lambda x: x.value)
                    a_item.asset_type = a_type
                    a_qual = st.number_input(f"Quality #{i+1}", min_value=0, max_value=4, value=a_item.quality, key=f"a_qual_{i}")
                    a_item.quality = a_qual
                else:
                    a_item.name = picked_a
                    a_def = ASSETS[picked_a]
                    a_item.asset_type = a_def.asset_type
                    a_item.quality = a_def.quality
                    a_item.traits = list(a_def.traits)
                    a_item.description = a_def.description

            with c_a2:
                st.markdown(f"**Type:** `{a_item.asset_type.value}` | **Quality:** `{a_item.quality}`")
                if a_item.traits:
                    st.write(f"**Traits:** {', '.join(a_item.traits)}")
                if a_item.description:
                    st.write(f"*{a_item.description}*")
            st.markdown("---")

    # TAB 7: AMBITION & DETAILS
    with tabs[6]:
        st.subheader("Step 8: Finishing Touches & Ambition")
        highest_drive = max(char.drives, key=char.drives.get)
        st.info(f"Your highest drive is **{highest_drive.value} ({char.get_drive(highest_drive)})**. Ambitions are typically tied to this drive.")

        amb_suggestions = AMBITION_EXAMPLES.get(highest_drive, [])
        options = amb_suggestions + (["Custom Ambition..."] if char.ambition not in amb_suggestions else ["Custom Ambition..."])
        amb_idx = options.index(char.ambition) if char.ambition in options else len(options) - 1
        picked_amb = st.selectbox("Ambition", options, index=amb_idx)
        if picked_amb == "Custom Ambition...":
            char.ambition = st.text_input("Enter Custom Ambition", value=char.ambition if char.ambition != "Custom Ambition..." else "")
        else:
            char.ambition = picked_amb

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            char.player_name = st.text_input("Player Name", value=char.player_name)
            char.appearance = st.text_area("Appearance", value=char.appearance, height=100)
            char.personality = st.text_area("Personality", value=char.personality, height=100)
        with col_d2:
            char.relationships = st.text_area("Relationships & Allies", value=char.relationships, height=100)
            char.notes = st.text_area("Notes & Backstory", value=char.notes, height=100)

    # TAB 8: CHARACTER SHEET PREVIEW
    with tabs[7]:
        st.subheader("Character Sheet Preview & Export")
        st.markdown(f"### {char.name} — *{char.concept}*")

        col_prev1, col_prev2 = st.columns(2)
        with col_prev1:
            st.markdown("#### Skills & Focuses")
            for sk in SkillName:
                f_list = [f.name for f in char.focuses if f.skill == sk]
                f_str = f" ({', '.join(f_list)})" if f_list else ""
                st.write(f"• **{sk.value}:** {char.get_skill(sk)}{f_str}")

            st.markdown("#### Drives & Statements")
            for d, score in sorted(char.drives.items(), key=lambda x: x[1], reverse=True):
                stmt = char.drive_statements.get(d, "")
                stmt_str = f' — *"{stmt}"*' if stmt else ""
                st.write(f"• **{d.value}:** {score}{stmt_str}")

        with col_prev2:
            st.markdown("#### Talents")
            for t in char.talents:
                st.write(f"• **{t.display_name}:** {t.description[:120]}...")

            st.markdown("#### Assets")
            for a in char.assets:
                q_str = f" [Q{a.quality}]" if a.quality > 0 else ""
                st.write(f"• **{a.name}** ({a.asset_type.value}){q_str}")

        st.markdown("---")
        st.subheader("Download Character Sheet")
        c_dl1, c_dl2, c_dl3 = st.columns(3)
        with c_dl1:
            st.download_button(
                "📄 Download Printable HTML Sheet",
                data=character_to_html(char),
                file_name=f"{char.name.replace(' ', '_')}_sheet.html",
                mime="text/html",
                use_container_width=True,
            )
        with c_dl2:
            st.download_button(
                "📝 Download Markdown (.md)",
                data=character_to_markdown(char),
                file_name=f"{char.name.replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with c_dl3:
            st.download_button(
                "💾 Download JSON Data (.json)",
                data=character_to_json(char),
                file_name=f"{char.name.replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True,
            )

# -------------------------------------------------------------
# MODE 2: INSTANT RANDOM CHARACTER
# -------------------------------------------------------------
elif mode == "🎲 Instant Random Character":
    st.subheader("🎲 Generate a Random Player Character")
    st.caption("Generate a fully rule-compliant character with coherent archetype, talents, focuses, drives, and assets.")

    c_f1, c_f2, c_f3 = st.columns(3)
    with c_f1:
        faction_choices = ["Any Faction"] + [f.value for f in FactionType]
        chosen_fac_str = st.selectbox("Faction Filter", faction_choices)
        fac_override = None
        if chosen_fac_str != "Any Faction":
            fac_override = next(f for f in FactionType if f.value == chosen_fac_str)

    with c_f2:
        arch_choices = ["Any Archetype"] + get_all_archetype_names()
        chosen_arch = st.selectbox("Archetype Filter", arch_choices)
        arch_override = None if chosen_arch == "Any Archetype" else chosen_arch

    with c_f3:
        house_choices = ["Any House"] + CANON_HOUSES
        chosen_h = st.selectbox("House Filter", house_choices)
        house_override = None if chosen_h == "Any House" else chosen_h

    if st.button("✨ Generate New Character", type="primary", use_container_width=True):
        st.session_state["character"] = generate_random_character(
            faction=fac_override,
            archetype_name=arch_override,
            house=house_override,
        )
        st.rerun()

    char = st.session_state["character"]
    st.markdown("---")
    st.markdown(f"### {char.name}")
    st.markdown(f"*{char.concept}*")

    st.markdown(
        f'<span class="badge-pill">{char.house}</span>'
        f'<span class="badge-pill">{char.homeworld}</span>'
        f'<span class="badge-pill">{char.archetype}</span>'
        f'<span class="badge-pill">{char.faction.value}</span>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Skills & Focuses")
        for sk, val in char.skills.items():
            f_list = [f.name for f in char.focuses if f.skill == sk]
            f_str = f" *({', '.join(f_list)})*" if f_list else ""
            st.write(f"• **{sk.value}:** {val}{f_str}")

        st.markdown("#### Drives & Statements")
        for d, score in sorted(char.drives.items(), key=lambda x: x[1], reverse=True):
            stmt = char.drive_statements.get(d, "")
            stmt_str = f' — *"{stmt}"*' if stmt else ""
            st.write(f"• **{d.value}:** {score}{stmt_str}")

    with c2:
        st.markdown("#### Talents")
        for t in char.talents:
            st.write(f"• **{t.display_name}:** {t.description}")

        st.markdown("#### Assets")
        for a in char.assets:
            st.write(f"• **{a.name}** ({a.asset_type.value}) — {a.description}")

    st.markdown("---")
    c_dl1, c_dl2, c_dl3 = st.columns(3)
    with c_dl1:
        st.download_button("📄 Download Printable HTML", character_to_html(char), f"{char.name}.html", "text/html", use_container_width=True)
    with c_dl2:
        st.download_button("📝 Download Markdown", character_to_markdown(char), f"{char.name}.md", "text/markdown", use_container_width=True)
    with c_dl3:
        st.download_button("💾 Download JSON", character_to_json(char), f"{char.name}.json", "application/json", use_container_width=True)

# -------------------------------------------------------------
# MODE 3: SUPPORTING NPC GENERATOR
# -------------------------------------------------------------
elif mode == "👥 Supporting NPC Generator":
    st.subheader("👥 Supporting Character (NPC) Generator")
    st.caption("Generate stat blocks for Minor and Notable Supporting Characters during game sessions (Core Rules p. 145-146).")

    col_npc1, col_npc2, col_npc3 = st.columns(3)
    with col_npc1:
        npc_type = st.radio("NPC Tier", ["Minor Supporting Character", "Notable Supporting Character"])
    with col_npc2:
        npc_role = st.selectbox("Role Template", [
            "House Guard",
            "Ornithopter Pilot",
            "House Diplomat",
            "Sietch Guide",
            "Cryptographer",
            "Field Medic",
            "Infiltrator Scout",
            "Quartermaster",
        ])
    with col_npc3:
        npc_house = st.selectbox("House Allegiance", CANON_HOUSES)

    if st.button("⚔️ Generate NPC", type="primary"):
        if npc_type == "Minor Supporting Character":
            st.session_state["npc"] = generate_minor_npc(role_name=npc_role, house=npc_house)
        else:
            st.session_state["npc"] = generate_notable_npc(role_name=npc_role, house=npc_house)

    if "npc" in st.session_state:
        npc: Character = st.session_state["npc"]
        st.markdown("---")
        st.markdown(f"### {npc.name}")
        st.write(f"**Concept:** {npc.concept} | **House:** {npc.house} | **Trait:** `{npc.personal_trait}`")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Skills & Focuses")
            for sk, val in npc.skills.items():
                f_list = [f.name for f in npc.focuses if f.skill == sk]
                f_str = f" *({', '.join(f_list)})*" if f_list else ""
                st.write(f"• **{sk.value}:** {val}{f_str}")
            
            if npc.character_type == CharacterType.MINOR_NPC:
                st.markdown(f"#### Single Drive Rating: **{npc.get_drive(DriveName.DUTY)}**")
            else:
                st.markdown("#### Drives")
                for d, val in sorted(npc.drives.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"• **{d.value}:** {val}")

        with c2:
            if npc.talents:
                st.markdown("#### Talents")
                for t in npc.talents:
                    st.write(f"• **{t.name}:** {t.description}")

            st.markdown("#### Assets")
            for a in npc.assets:
                st.write(f"• **{a.name}** ({a.asset_type.value})")

        st.download_button("📄 Download NPC HTML", character_to_html(npc), f"{npc.name}.html", "text/html")

# -------------------------------------------------------------
# MODE 4: CHARACTER VAULT & EXPORT
# -------------------------------------------------------------
elif mode == "📂 Character Vault & Export":
    st.subheader("📂 Character Vault & File Management")

    uploaded = st.file_uploader("Upload Saved Character (.json)", type=["json"])
    if uploaded is not None:
        try:
            content = uploaded.read().decode("utf-8")
            loaded_char = character_from_json(content)
            st.session_state["character"] = loaded_char
            st.success(f"Successfully loaded '{loaded_char.name}'!")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to parse character file: {e}")

    st.markdown("---")
    st.subheader("Export Current Active Character")
    st.markdown(f"Active Character: **{char.name}** ({char.concept})")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("📄 Standalone HTML Sheet", character_to_html(char), f"{char.name}.html", "text/html", use_container_width=True)
    with c2:
        st.download_button("📝 Markdown File (.md)", character_to_markdown(char), f"{char.name}.md", "text/markdown", use_container_width=True)
    with c3:
        st.download_button("💾 JSON Save File (.json)", character_to_json(char), f"{char.name}.json", "application/json", use_container_width=True)

# -------------------------------------------------------------
# MODE 5: ABOUT & CREDITS
# -------------------------------------------------------------
elif mode == "ℹ️ About & Credits":
    st.subheader("ℹ️ About the Application")
    st.markdown("""
    Welcome to the **Dune: Adventures in the Imperium Character Generator & Sheet Architect**!
    
    This application is an interactive digital companion designed for players and gamemasters of Modiphius Entertainment's tabletop roleplaying game ***Dune: Adventures in the Imperium*** (2d20 System).
    
    ### 🌟 Core Features
    - **Step-by-Step Character Creation**: Implements the official planned creation pipeline (Steps 1–8: Concept, Archetype, Skills, Focuses, Talents, Drives & Statements, Assets, and Ambition).
    - **Official 2d20 Rulebook Compliance**: Real-time validation checking skill totals (28 points), bounds (4–8), primary/secondary baselines, mandatory faction talents, drive rankings (`[8, 7, 6, 5, 4]`), and starting assets.
    - **Comprehensive Data Library**: All 20 canonical archetypes, 5 faction templates, 55 talents with rules text, standard focuses, and assets.
    - **Random PC & NPC Generators**: One-click generation of fully compliant player characters and supporting characters (*Minor* and *Notable* NPCs).
    - **Multi-Format Exporting**: Save to JSON, export to Markdown, and print/save to styled PDF character sheets.
    """)

    st.markdown("---")
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.subheader("⚖️ Copyrights & Trademarks")
        st.markdown("""
        - ***Dune: Adventures in the Imperium*** is published by **Modiphius Entertainment** in partnership with **Legendary Entertainment**.
        - **Dune** is a trademark or registered trademark of **Herbert Properties LLC**. All setting lore, faction names, character concepts, and related intellectual property are © Herbert Properties LLC and Legendary Entertainment.
        - **Unofficial Fan Companion**: This software application is an independent, fan-made utility created solely for personal recreational use. It is **not** affiliated with, produced by, or endorsed by Modiphius Entertainment, Legendary Entertainment, or Herbert Properties LLC.
        """)

    with col_c2:
        st.subheader("👥 Credits & Acknowledgments")
        st.markdown("""
        - **Frank Herbert**: For imagining the breathtaking, intricate universe of Arrakis and the Imperium.
        - **Modiphius Entertainment Team**: Nathan Dowdell, Simon Berman, Jack Norris, Jason Durall, Chris Birch, and the entire writing and design team behind the 2d20 System adaptation of Dune.
        """)

    st.markdown("---")
    st.subheader("📄 License: Creative Commons (CC BY-NC 4.0)")
    st.markdown("""
    This fan project is made available under the terms of the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.
    
    - **You are free to**:
      - **Share**: Copy and redistribute the material in any medium or format.
      - **Adapt**: Remix, transform, and build upon the material.
    - **Under the following terms**:
      - **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made.
      - **NonCommercial**: You may **not** use this material for commercial purposes or financial gain.
    
    For full legal code and details, visit [Creative Commons CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
    """)

