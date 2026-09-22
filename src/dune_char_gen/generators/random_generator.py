"""Intelligent random PC generator respecting all Dune 2d20 creation rules."""

import random
from typing import Optional, List
from dune_char_gen.models.character import Character, FocusItem, TalentItem, AssetItem
from dune_char_gen.models.enums import SkillName, DriveName, FactionType, AssetType, CharacterType
from dune_char_gen.data.archetypes import ARCHETYPES, get_archetype, get_all_archetype_names
from dune_char_gen.data.factions import FACTION_TEMPLATES, get_faction_template
from dune_char_gen.data.skills_and_focuses import STANDARD_FOCUSES
from dune_char_gen.data.talents import TALENTS, get_talent, get_talents_for_faction
from dune_char_gen.data.drives import DRIVE_STATEMENTS, AMBITION_EXAMPLES
from dune_char_gen.data.assets import ASSETS, get_all_asset_names
from dune_char_gen.data.houses import CANON_HOUSES, HOMEWORLDS, HOUSE_ROLES, PERSONAL_TRAITS
from dune_char_gen.data.names import generate_dune_name, TITLES_BY_FACTION


def generate_random_character(
    faction: Optional[FactionType] = None,
    archetype_name: Optional[str] = None,
    house: Optional[str] = None,
    homeworld: Optional[str] = None,
    player_name: str = "",
) -> Character:
    """Generate a fully rule-compliant, thematic Dune 2d20 player character."""
    
    # 1. Determine Faction
    if faction is None:
        # Bias slightly toward standard House Retainer, but include factions
        faction_pool = [
            FactionType.NONE,
            FactionType.NONE,
            FactionType.BENE_GESSERIT,
            FactionType.FREMEN,
            FactionType.MENTAT,
            FactionType.SPACING_GUILD,
            FactionType.SUK_DOCTOR,
        ]
        faction = random.choice(faction_pool)
    
    fac_template = get_faction_template(faction)
    faction_trait = fac_template.additional_trait

    # 2. Determine Archetype
    if archetype_name is None:
        if fac_template.suggested_archetypes:
            # 80% chance to pick a suggested archetype for the faction
            if random.random() < 0.8:
                archetype_name = random.choice(fac_template.suggested_archetypes)
            else:
                archetype_name = random.choice(get_all_archetype_names())
        else:
            archetype_name = random.choice(get_all_archetype_names())
    
    arch_def = get_archetype(archetype_name)
    if arch_def is None:
        archetype_name = "Warrior"
        arch_def = get_archetype("Warrior")

    # 3. Determine House & Homeworld
    if house is None:
        if faction == FactionType.FREMEN:
            house = "Independent / Fremen Tribe"
        else:
            house = random.choice([h for h in CANON_HOUSES if "Fremen" not in h])

    if homeworld is None:
        if faction == FactionType.FREMEN:
            homeworld = "Arrakis (Dune)"
        elif faction == FactionType.BENE_GESSERIT and random.random() < 0.3:
            homeworld = "Wallach IX"
        elif "Atreides" in house:
            homeworld = "Caladan"
        elif "Harkonnen" in house:
            homeworld = "Giedi Prime"
        elif "Corrino" in house:
            homeworld = "Kaitain"
        else:
            homeworld = random.choice(HOMEWORLDS)

    # 4. Generate Name & Concept
    name = generate_dune_name(faction)
    house_role = random.choice(HOUSE_ROLES)
    personal_trait = random.choice(PERSONAL_TRAITS)
    concept = f"{personal_trait} {archetype_name} serving {house} as {house_role}."

    # 5. Distribute Skills (Base: Primary=6, Secondary=5, others=4, +5 free points, max 8)
    skills = {
        SkillName.BATTLE: 4,
        SkillName.COMMUNICATE: 4,
        SkillName.DISCIPLINE: 4,
        SkillName.MOVE: 4,
        SkillName.UNDERSTAND: 4,
    }
    skills[arch_def.primary_skill] = 6
    skills[arch_def.secondary_skill] = 5

    # 5 points to distribute freely without exceeding 8
    points_to_spend = 5
    # Weighted preference towards primary and secondary skills
    candidates = [
        arch_def.primary_skill,
        arch_def.primary_skill,
        arch_def.secondary_skill,
        arch_def.secondary_skill,
        SkillName.BATTLE,
        SkillName.COMMUNICATE,
        SkillName.DISCIPLINE,
        SkillName.MOVE,
        SkillName.UNDERSTAND,
    ]
    while points_to_spend > 0:
        sk = random.choice(candidates)
        if skills[sk] < 8:
            skills[sk] += 1
            points_to_spend -= 1

    # 6. Choose 4 Focuses (at least 1 in primary skill)
    focuses: List[FocusItem] = []
    # Try using suggested focuses first
    primary_suggestions = [
        f for f in arch_def.suggested_focuses
        if f in STANDARD_FOCUSES.get(arch_def.primary_skill, [])
    ]
    if primary_suggestions:
        focuses.append(FocusItem(name=primary_suggestions[0], skill=arch_def.primary_skill))
    else:
        # Pick from standard primary skill focuses
        f_name = random.choice(STANDARD_FOCUSES[arch_def.primary_skill])
        focuses.append(FocusItem(name=f_name, skill=arch_def.primary_skill))

    # Add second focus (preferably secondary skill suggestion or general suggestion)
    sec_suggestions = [
        f for f in arch_def.suggested_focuses
        if f not in [x.name for x in focuses]
    ]
    if sec_suggestions:
        f_name = sec_suggestions[0]
        # Determine which skill this focus belongs to
        assigned_skill = arch_def.secondary_skill
        for sk_candidate, f_list in STANDARD_FOCUSES.items():
            if f_name in f_list:
                assigned_skill = sk_candidate
                break
        focuses.append(FocusItem(name=f_name, skill=assigned_skill))

    # Fill remaining focuses up to 4
    skill_priority = [arch_def.primary_skill, arch_def.secondary_skill] + [
        s for s in SkillName if s not in (arch_def.primary_skill, arch_def.secondary_skill)
    ]
    while len(focuses) < 4:
        sk = random.choice(skill_priority)
        available = [f for f in STANDARD_FOCUSES[sk] if f not in [x.name for x in focuses]]
        if available:
            f_name = random.choice(available)
            focuses.append(FocusItem(name=f_name, skill=sk))

    # 7. Select 3 Talents (respecting faction mandatory rules)
    talents: List[TalentItem] = []
    chosen_names = set()

    # Handle mandatory faction talents
    if fac_template.mandatory_talents:
        if fac_template.require_all_mandatory:
            for mt in fac_template.mandatory_talents:
                t_def = get_talent(mt)
                desc = t_def.rules if t_def else ""
                talents.append(TalentItem(name=mt, description=desc))
                chosen_names.add(mt)
        else:
            # Pick one mandatory talent from the list
            chosen_mt = random.choice(fac_template.mandatory_talents)
            t_def = get_talent(chosen_mt)
            desc = t_def.rules if t_def else ""
            talents.append(TalentItem(name=chosen_mt, description=desc))
            chosen_names.add(chosen_mt)

    # Suggest archetype talent if not yet taken
    if arch_def.suggested_talent and arch_def.suggested_talent not in chosen_names:
        t_def = get_talent(arch_def.suggested_talent)
        if t_def and (t_def.faction_requirement is None or (faction and t_def.faction_requirement.lower() in faction.value.lower())):
            talents.append(TalentItem(name=t_def.name, description=t_def.rules))
            chosen_names.add(t_def.name)

    # Fill remaining talents from available pool
    available_talents = get_talents_for_faction(faction.value if faction != FactionType.NONE else None)
    pool = [t for t in available_talents if t.name not in chosen_names]
    while len(talents) < 3 and pool:
        picked = random.choice(pool)
        spec = None
        if picked.skill_param:
            spec = random.choice([arch_def.primary_skill.value, arch_def.secondary_skill.value])
        elif picked.drive_param:
            spec = "Duty"
        talents.append(TalentItem(name=picked.name, specialization=spec, description=picked.rules))
        chosen_names.add(picked.name)
        pool = [t for t in pool if t.name not in chosen_names]

    # 8. Drives & Statements ([8, 7, 6, 5, 4])
    all_drives = [DriveName.DUTY, DriveName.FAITH, DriveName.JUSTICE, DriveName.POWER, DriveName.TRUTH]
    values = [8, 7, 6, 5, 4]
    random.shuffle(values)
    drives = {all_drives[i]: values[i] for i in range(5)}

    # Top 3 drives (ratings 8, 7, 6) get statements
    drive_statements = {}
    top_drives = [d for d, val in drives.items() if val >= 6]
    for d in top_drives:
        st_pool = DRIVE_STATEMENTS.get(d, ["I will uphold my ideals."])
        drive_statements[d] = random.choice(st_pool)

    # 9. Ambition (based on highest drive = 8)
    highest_drive = max(drives, key=drives.get)
    ambition_pool = AMBITION_EXAMPLES.get(highest_drive, ["Bring glory and renown to my House."])
    ambition = random.choice(ambition_pool)

    # 10. Assets (3 total, at least 1 tangible)
    assets: List[AssetItem] = []
    # Pick 1 tangible weapon/gear
    tangible_names = [k for k, v in ASSETS.items() if v.asset_type == AssetType.TANGIBLE]
    # Thematic picks: Fremen gets Crysknife/Stillsuit; Bene Gesserit gets Poison Snooper/Blade; Duelist gets Kindjal/Personal Shield
    if faction == FactionType.FREMEN:
        tangible_priority = ["Crysknife", "Stillsuit", "Fremkit", "Maula Pistol"]
    elif archetype_name == "Duelist":
        tangible_priority = ["Kindjal", "Personal Shield", "Blade", "Bodkin"]
    elif faction == FactionType.MENTAT:
        tangible_priority = ["Sapho Juice", "Filmbook & Reader", "Poison Snooper"]
    else:
        tangible_priority = ["Kindjal", "Personal Shield", "Blade", "Maula Pistol", "Poison Snooper"]

    first_asset_name = random.choice(tangible_priority)
    first_def = ASSETS[first_asset_name]
    assets.append(AssetItem(
        name=first_def.name,
        asset_type=first_def.asset_type,
        quality=first_def.quality,
        traits=list(first_def.traits),
        description=first_def.description,
    ))

    # Pick 2nd asset (can be tangible or intangible)
    all_asset_keys = list(ASSETS.keys())
    remaining_keys = [k for k in all_asset_keys if k != first_asset_name]
    
    # Biased toward 1 intangible (contact, favor, secrets)
    intangible_keys = [k for k, v in ASSETS.items() if v.asset_type == AssetType.INTANGIBLE and k != first_asset_name]
    if intangible_keys:
        second_name = random.choice(intangible_keys)
    else:
        second_name = random.choice(remaining_keys)
    
    sec_def = ASSETS[second_name]
    assets.append(AssetItem(
        name=sec_def.name,
        asset_type=sec_def.asset_type,
        quality=sec_def.quality,
        traits=list(sec_def.traits),
        description=sec_def.description,
    ))

    # Pick 3rd asset
    remaining_keys = [k for k in remaining_keys if k != second_name]
    third_name = random.choice(remaining_keys)
    third_def = ASSETS[third_name]
    assets.append(AssetItem(
        name=third_def.name,
        asset_type=third_def.asset_type,
        quality=third_def.quality,
        traits=list(third_def.traits),
        description=third_def.description,
    ))

    # Bonus assets for Specialist or Improved Resources
    bonus_assets = sum(2 for t in talents if t.name in ["Improved Resources", "Specialist"] or t.name.startswith("Specialist"))
    while len(assets) < 3 + bonus_assets:
        rem = [k for k in all_asset_keys if k not in [a.name for a in assets]]
        if not rem:
            break
        extra_name = random.choice(rem)
        extra_def = ASSETS[extra_name]
        assets.append(AssetItem(
            name=extra_def.name,
            asset_type=extra_def.asset_type,
            quality=extra_def.quality,
            traits=list(extra_def.traits),
            description=extra_def.description,
        ))

    return Character(
        name=name,
        player_name=player_name,
        concept=concept,
        character_type=CharacterType.PLAYER_CHARACTER,
        house=house,
        homeworld=homeworld,
        house_role=house_role,
        house_trait="",
        faction=faction,
        faction_trait=faction_trait,
        archetype=archetype_name,
        archetype_trait=archetype_name,
        personal_trait=personal_trait,
        skills=skills,
        focuses=focuses,
        drives=drives,
        drive_statements=drive_statements,
        ambition=ambition,
        determination=1,
        talents=talents,
        assets=assets,
        appearance="Dressed in finely-tailored attire appropriate to station with desert-worn gear at hand.",
        personality=f"{personal_trait.capitalize()}, perceptive, and deeply committed to their personal code.",
        relationships=f"Sworn in service to {house}; answers to the high officers of the House.",
        notes="Generated character for Dune: Adventures in the Imperium.",
    )
