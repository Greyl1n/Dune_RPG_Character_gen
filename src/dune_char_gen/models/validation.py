"""Validation engine enforcing official 2d20 rules for Dune: Adventures in the Imperium."""

from dataclasses import dataclass, field
from typing import Dict, List
from dune_char_gen.models.character import Character
from dune_char_gen.models.enums import SkillName, DriveName, FactionType, AssetType, CharacterType
from dune_char_gen.data.archetypes import get_archetype
from dune_char_gen.data.factions import get_faction_template
from dune_char_gen.data.talents import get_talent


@dataclass
class ValidationReport:
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    checks: Dict[str, bool] = field(default_factory=dict)


def validate_character(char: Character) -> ValidationReport:
    """Validate character against Dune 2d20 creation rules."""
    errors: List[str] = []
    warnings: List[str] = []
    checks: Dict[str, bool] = {}

    if char.character_type != CharacterType.PLAYER_CHARACTER:
        # Minor or Notable NPC validation (relaxed)
        checks["NPC Basic Stats"] = True
        return ValidationReport(is_valid=True, errors=[], warnings=[], checks=checks)

    # 1. Skills Validation
    skill_sum = sum(char.skills.values())
    skills_sum_ok = (skill_sum == 28)
    checks["Skill Points Total (28)"] = skills_sum_ok
    if not skills_sum_ok:
        errors.append(f"Skill points total is {skill_sum}, but must be exactly 28 (Base 6, 5, 4, 4, 4 + 5 free points).")

    skill_bounds_ok = all(4 <= val <= 8 for val in char.skills.values())
    checks["Skill Range (4-8)"] = skill_bounds_ok
    if not skill_bounds_ok:
        for sk, val in char.skills.items():
            if val < 4 or val > 8:
                errors.append(f"Skill {sk.value} is {val}; must be between 4 and 8.")

    # Archetype primary/secondary check
    archetype_def = get_archetype(char.archetype)
    if archetype_def:
        primary_ok = char.get_skill(archetype_def.primary_skill) >= 6
        secondary_ok = char.get_skill(archetype_def.secondary_skill) >= 5
        checks[f"Primary Skill ({archetype_def.primary_skill.value} >= 6)"] = primary_ok
        checks[f"Secondary Skill ({archetype_def.secondary_skill.value} >= 5)"] = secondary_ok
        if not primary_ok:
            errors.append(
                f"Archetype {char.archetype} requires primary skill {archetype_def.primary_skill.value} to be at least 6."
            )
        if not secondary_ok:
            errors.append(
                f"Archetype {char.archetype} requires secondary skill {archetype_def.secondary_skill.value} to be at least 5."
            )
    else:
        checks["Archetype Recognized"] = False
        errors.append(f"Unknown archetype '{char.archetype}'.")

    # 2. Focuses Validation
    focus_count_ok = (len(char.focuses) == 4)
    checks["4 Focuses Chosen"] = focus_count_ok
    if not focus_count_ok:
        errors.append(f"Character has {len(char.focuses)} focuses; must have exactly 4.")

    if archetype_def:
        primary_focuses = [f for f in char.focuses if f.skill == archetype_def.primary_skill]
        primary_focus_ok = (len(primary_focuses) >= 1)
        checks[f"Focus in Primary Skill ({archetype_def.primary_skill.value})"] = primary_focus_ok
        if not primary_focus_ok:
            errors.append(
                f"At least one focus must be assigned to the primary skill ({archetype_def.primary_skill.value})."
            )

    # 3. Talents Validation
    talent_count_ok = (len(char.talents) == 3)
    checks["3 Talents Chosen"] = talent_count_ok
    if not talent_count_ok:
        errors.append(f"Character has {len(char.talents)} talents; must have exactly 3.")

    # Faction talent restrictions
    fac_template = get_faction_template(char.faction)
    char_talent_names = [t.name for t in char.talents]

    faction_talent_ok = True
    if fac_template.mandatory_talents:
        if fac_template.require_all_mandatory:
            for mt in fac_template.mandatory_talents:
                if mt not in char_talent_names:
                    faction_talent_ok = False
                    errors.append(f"{fac_template.name} requires the mandatory talent '{mt}'.")
        else:
            has_one = any(mt in char_talent_names for mt in fac_template.mandatory_talents)
            if not has_one:
                faction_talent_ok = False
                errors.append(
                    f"{fac_template.name} requires at least one of these talents: "
                    f"{', '.join(fac_template.mandatory_talents)}."
                )
    checks["Faction Mandatory Talents Met"] = faction_talent_ok

    # Validate that non-faction characters don't pick restricted faction talents
    for t_item in char.talents:
        t_def = get_talent(t_item.name)
        if t_def and t_def.faction_requirement:
            if char.faction == FactionType.NONE or t_def.faction_requirement.lower() not in char.faction.value.lower():
                errors.append(
                    f"Talent '{t_item.name}' requires faction '{t_def.faction_requirement}', "
                    f"which does not match character's faction '{char.faction.value}'."
                )

    # 4. Drives Validation
    drive_values = sorted(list(char.drives.values()))
    expected_values = [4, 5, 6, 7, 8]
    drives_ok = (drive_values == expected_values)
    checks["Drives Assigned [8, 7, 6, 5, 4]"] = drives_ok
    if not drives_ok:
        errors.append(f"Drives must be assigned exactly [8, 7, 6, 5, 4]. Current: {list(char.drives.values())}.")

    # 5. Drive Statements Validation
    top_drives = [d for d, val in char.drives.items() if val >= 6]
    missing_statements = []
    for d in top_drives:
        stmt = char.drive_statements.get(d, "").strip()
        if not stmt:
            missing_statements.append(d.value)
    
    statements_ok = (len(missing_statements) == 0 and len(top_drives) == 3)
    checks["3 Drive Statements (for ratings 8, 7, 6)"] = statements_ok
    if missing_statements:
        errors.append(f"Missing drive statements for top drives: {', '.join(missing_statements)}.")

    # 6. Assets Validation
    bonus_assets = sum(2 for t in char.talents if t.name in ["Improved Resources", "Specialist"] or t.name.startswith("Specialist"))
    expected_assets = 3 + bonus_assets
    assets_count_ok = (len(char.assets) == expected_assets)
    label = f"{expected_assets} Assets ({bonus_assets} bonus)" if bonus_assets > 0 else "3 Starting Assets"
    checks[label] = assets_count_ok
    if not assets_count_ok:
        extra_note = f" (3 standard + {bonus_assets} from talents)" if bonus_assets > 0 else ""
        errors.append(f"Character has {len(char.assets)} assets; expected {expected_assets}{extra_note}.")

    tangible_count = sum(1 for a in char.assets if a.asset_type == AssetType.TANGIBLE)
    tangible_ok = (tangible_count >= 1)
    checks["At Least 1 Tangible Asset"] = tangible_ok
    if not tangible_ok:
        errors.append("At least one starting asset must be Tangible.")

    # 7. Ambition & Details
    ambition_ok = bool(char.ambition.strip())
    checks["Ambition Defined"] = ambition_ok
    if not ambition_ok:
        warnings.append("Ambition is currently empty. A long-term goal tied to the highest drive is recommended.")

    name_ok = bool(char.name.strip() and char.name != "New Character")
    checks["Character Name Set"] = name_ok
    if not name_ok:
        warnings.append("Character has no custom name specified.")

    is_valid = len(errors) == 0
    return ValidationReport(
        is_valid=is_valid,
        errors=errors,
        warnings=warnings,
        checks=checks,
    )
