"""Supporting Character (NPC) generator from Dune: Adventures in the Imperium (p. 145-146)."""

import random
from typing import Optional, List
from dune_char_gen.models.character import Character, FocusItem, TalentItem, AssetItem
from dune_char_gen.models.enums import SkillName, DriveName, FactionType, AssetType, CharacterType
from dune_char_gen.data.skills_and_focuses import STANDARD_FOCUSES
from dune_char_gen.data.assets import ASSETS
from dune_char_gen.data.talents import get_all_talent_names, get_talent
from dune_char_gen.data.names import generate_dune_name

NPC_ROLES = [
    ("House Guard", SkillName.BATTLE, "Blade", "Protector"),
    ("Ornithopter Pilot", SkillName.MOVE, "Personal Shield", "Pilot"),
    ("House Diplomat", SkillName.COMMUNICATE, "House Retainer Contract", "Envoy"),
    ("Sietch Guide", SkillName.MOVE, "Stillsuit", "Fremen"),
    ("Cryptographer", SkillName.UNDERSTAND, "Filmbook & Reader", "Scholar"),
    ("Field Medic", SkillName.UNDERSTAND, "Poison Snooper", "Physician"),
    ("Infiltrator Scout", SkillName.DISCIPLINE, "Bodkin", "Infiltrator"),
    ("Quartermaster", SkillName.COMMUNICATE, "CHOAM Trading Permit", "Steward"),
]


def generate_minor_npc(
    role_name: Optional[str] = None,
    house: str = "House Atreides",
    drive_rating: int = 5,
) -> Character:
    """Generate a Minor Supporting Character per Core Rules p. 145-146."""
    if not role_name:
        role_tuple = random.choice(NPC_ROLES)
        role_name, primary_sk, asset_name, trait_name = role_tuple
    else:
        role_tuple = next((r for r in NPC_ROLES if r[0].lower() == role_name.lower()), None)
        if role_tuple:
            _, primary_sk, asset_name, trait_name = role_tuple
        else:
            primary_sk = SkillName.BATTLE
            asset_name = "Blade"
            trait_name = role_name

    # Skills: One at 6, two at 5, two at 4
    all_skills = list(SkillName)
    remaining_skills = [s for s in all_skills if s != primary_sk]
    random.shuffle(remaining_skills)
    
    skills = {primary_sk: 6}
    skills[remaining_skills[0]] = 5
    skills[remaining_skills[1]] = 5
    skills[remaining_skills[2]] = 4
    skills[remaining_skills[3]] = 4

    # Focus: 1 focus for the skill at 6
    focus_pool = STANDARD_FOCUSES.get(primary_sk, ["General"])
    focus = FocusItem(name=random.choice(focus_pool), skill=primary_sk)

    # Asset: 1 basic asset
    asset_def = ASSETS.get(asset_name, ASSETS["Blade"])
    asset = AssetItem(
        name=asset_def.name,
        asset_type=asset_def.asset_type,
        quality=asset_def.quality,
        traits=list(asset_def.traits),
        description=asset_def.description,
    )

    name = generate_dune_name()

    return Character(
        name=f"{name} ({role_name})",
        concept=f"Minor NPC: {role_name} serving {house}",
        character_type=CharacterType.MINOR_NPC,
        house=house,
        personal_trait=trait_name,
        archetype=role_name,
        archetype_trait=trait_name,
        skills=skills,
        focuses=[focus],
        drives={
            DriveName.DUTY: drive_rating,
            DriveName.FAITH: drive_rating,
            DriveName.JUSTICE: drive_rating,
            DriveName.POWER: drive_rating,
            DriveName.TRUTH: drive_rating,
        },
        drive_statements={},
        ambition=f"Faithfully perform duties as {role_name}.",
        talents=[],
        assets=[asset],
        notes="Minor supporting character. Uses single Drive rating for tests.",
    )


def generate_notable_npc(
    role_name: Optional[str] = None,
    house: str = "House Atreides",
) -> Character:
    """Generate a Notable Supporting Character per Core Rules p. 146."""
    if not role_name:
        role_tuple = random.choice(NPC_ROLES)
        role_name, primary_sk, asset_name, trait_name = role_tuple
    else:
        role_tuple = next((r for r in NPC_ROLES if r[0].lower() == role_name.lower()), None)
        if role_tuple:
            _, primary_sk, asset_name, trait_name = role_tuple
        else:
            primary_sk = SkillName.BATTLE
            asset_name = "Blade"
            trait_name = role_name

    # Skills: One at 7, one at 6, one at 5, two at 4
    remaining = [s for s in SkillName if s != primary_sk]
    random.shuffle(remaining)
    skills = {
        primary_sk: 7,
        remaining[0]: 6,
        remaining[1]: 5,
        remaining[2]: 4,
        remaining[3]: 4,
    }

    # Focuses: 2 focuses (1 in top skill, 1 in secondary)
    f1 = FocusItem(name=random.choice(STANDARD_FOCUSES[primary_sk]), skill=primary_sk)
    f2 = FocusItem(name=random.choice(STANDARD_FOCUSES[remaining[0]]), skill=remaining[0])

    # Drives: 1 at 8, 1 at 7, 1 at 6, 2 at 5
    drive_names = list(DriveName)
    random.shuffle(drive_names)
    drives = {
        drive_names[0]: 8,
        drive_names[1]: 7,
        drive_names[2]: 6,
        drive_names[3]: 5,
        drive_names[4]: 5,
    }

    # Talent: 1 talent
    talents_pool = ["Advisor", "Bold", "Bolster", "Cool Under Pressure", "Master-at-Arms", "Nimble"]
    t_name = random.choice(talents_pool)
    t_def = get_talent(t_name)
    talent = TalentItem(name=t_name, description=t_def.rules if t_def else "")

    # Assets: 2 assets
    asset_def1 = ASSETS.get(asset_name, ASSETS["Blade"])
    asset1 = AssetItem(
        name=asset_def1.name,
        asset_type=asset_def1.asset_type,
        quality=asset_def1.quality,
        traits=list(asset_def1.traits),
        description=asset_def1.description,
    )
    asset_def2 = ASSETS["Personal Shield"] if asset_def1.name != "Personal Shield" else ASSETS["Old Friendship"]
    asset2 = AssetItem(
        name=asset_def2.name,
        asset_type=asset_def2.asset_type,
        quality=asset_def2.quality,
        traits=list(asset_def2.traits),
        description=asset_def2.description,
    )

    name = generate_dune_name()

    return Character(
        name=f"{name} (Notable {role_name})",
        concept=f"Notable NPC: {role_name} of {house}",
        character_type=CharacterType.NOTABLE_NPC,
        house=house,
        personal_trait=trait_name,
        archetype=role_name,
        archetype_trait=trait_name,
        skills=skills,
        focuses=[f1, f2],
        drives=drives,
        drive_statements={
            drive_names[0]: "I stand resolute in service.",
        },
        ambition=f"Advance the standing of {house}.",
        talents=[talent],
        assets=[asset1, asset2],
        notes="Notable supporting character (Costs 3 Momentum/Threat).",
    )
