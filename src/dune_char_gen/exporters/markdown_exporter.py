"""Markdown character sheet exporter for Dune: Adventures in the Imperium."""

from dune_char_gen.models.character import Character
from dune_char_gen.models.enums import SkillName, DriveName, FactionType


def character_to_markdown(char: Character) -> str:
    """Format character as a clean Markdown character sheet."""
    lines = []
    lines.append(f"# {char.name}")
    if char.concept:
        lines.append(f"*{char.concept}*\n")
    else:
        lines.append("")

    # Identity block
    lines.append("## Identity & Affiliations")
    lines.append(f"- **Character Type:** {char.character_type.value}")
    lines.append(f"- **House:** {char.house} (Homeworld: {char.homeworld})")
    lines.append(f"- **Role in House:** {char.house_role}")
    if char.faction != FactionType.NONE:
        lines.append(f"- **Faction:** {char.faction.value}")
    lines.append(f"- **Archetype:** {char.archetype}")
    lines.append(f"- **Traits:** {', '.join(char.all_traits) if char.all_traits else 'None'}")
    lines.append(f"- **Determination:** {char.determination}")
    lines.append("")

    # Ambition
    lines.append("## Ambition")
    lines.append(f"> {char.ambition if char.ambition else 'No ambition set'}\n")

    # Skills & Focuses
    lines.append("## Skills & Focuses")
    lines.append("| Skill | Score | Assigned Focuses |")
    lines.append("| :--- | :---: | :--- |")
    for sk in [SkillName.BATTLE, SkillName.COMMUNICATE, SkillName.DISCIPLINE, SkillName.MOVE, SkillName.UNDERSTAND]:
        score = char.get_skill(sk)
        f_list = [f.name for f in char.focuses if f.skill == sk]
        focuses_str = ", ".join(f_list) if f_list else "—"
        lines.append(f"| **{sk.value}** | **{score}** | {focuses_str} |")
    lines.append("")

    # Drives & Statements
    lines.append("## Drives & Statements")
    lines.append("| Drive | Score | Drive Statement |")
    lines.append("| :--- | :---: | :--- |")
    # Order by score descending
    sorted_drives = sorted(char.drives.items(), key=lambda x: x[1], reverse=True)
    for d, score in sorted_drives:
        statement = char.drive_statements.get(d, "—")
        lines.append(f"| **{d.value}** | **{score}** | *\"{statement}\"* |")
    lines.append("")

    # Talents
    lines.append("## Talents")
    if char.talents:
        for t in char.talents:
            lines.append(f"### {t.display_name}")
            if t.description:
                lines.append(f"{t.description}\n")
            else:
                lines.append("")
    else:
        lines.append("*No talents recorded.*\n")

    # Assets
    lines.append("## Starting Assets")
    if char.assets:
        for a in char.assets:
            traits_str = f" [{', '.join(a.traits)}]" if a.traits else ""
            quality_str = f" (Quality {a.quality})" if a.quality > 0 else ""
            lines.append(f"- **{a.name}** ({a.asset_type.value}){quality_str}{traits_str}")
            if a.description:
                lines.append(f"  *{a.description}*")
        lines.append("")
    else:
        lines.append("*No assets recorded.*\n")

    # Personal Details
    lines.append("## Personal Details")
    if char.appearance:
        lines.append(f"- **Appearance:** {char.appearance}")
    if char.personality:
        lines.append(f"- **Personality:** {char.personality}")
    if char.relationships:
        lines.append(f"- **Relationships:** {char.relationships}")
    if char.notes:
        lines.append(f"- **Notes:** {char.notes}")
    lines.append("")

    return "\n".join(lines)
