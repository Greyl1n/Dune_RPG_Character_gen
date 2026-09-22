"""Skills and standard Focuses catalog from Dune: Adventures in the Imperium core rules."""

from typing import Dict, List
from dune_char_gen.models.enums import SkillName

SKILL_DESCRIPTIONS: Dict[SkillName, str] = {
    SkillName.BATTLE: (
        "Describes combat prowess in personal, skirmish, and fleet actions. "
        "Includes martial arts, blade combat, shield use, ranged weaponry, and tactical prowess."
    ),
    SkillName.COMMUNICATE: (
        "Describes interpersonal capability, persuasion, diplomacy, charisma, deceit, "
        "and commanding presence in social and political spheres."
    ),
    SkillName.DISCIPLINE: (
        "Describes mental endurance, composure under pressure, willpower, stealth, "
        "focus, and resisting sensory, psychological, or physical shocks."
    ),
    SkillName.MOVE: (
        "Describes physical mobility, athletics, speed, piloting, agility, "
        "acrobatics, and maneuvering in hazardous environments."
    ),
    SkillName.UNDERSTAND: (
        "Describes analytical reasoning, intellect, academic scholarship, data appraisal, "
        "strategic awareness, and scientific or cultural knowledge."
    ),
}

STANDARD_FOCUSES: Dict[SkillName, List[str]] = {
    SkillName.BATTLE: [
        "Assassination",
        "Atomics",
        "Dirty Fighting",
        "Dueling",
        "Evasive Action",
        "Heavy Weapons",
        "Lasguns",
        "Long Blades",
        "Pistol",
        "Pistols",
        "Projectile Weapons",
        "Rifle",
        "Shield Fighting",
        "Short Blades",
        "Special Weapons",
        "Tactics",
        "Unarmed Combat",
    ],
    SkillName.COMMUNICATE: [
        "Acting",
        "Bartering",
        "Charm",
        "Deceit",
        "Diplomacy",
        "Disguise",
        "Empathy",
        "Etiquette",
        "Innuendo",
        "Inspiration",
        "Intimidation",
        "Leadership",
        "Musical Instrument",
        "Negotiation",
        "Oratory",
        "Persuasion",
        "Seduction",
    ],
    SkillName.DISCIPLINE: [
        "Attention to Detail",
        "Command",
        "Composure",
        "Concentration",
        "Espionage",
        "Faith",
        "Infiltration",
        "Iron Will",
        "Meditation",
        "Observe",
        "Precision",
        "Resolve",
        "Self-Control",
        "Survival (Desert)",
        "Survival (Jungle)",
        "Survival (Urban)",
        "Survival (Arctic)",
    ],
    SkillName.MOVE: [
        "Acrobatics",
        "Athletics",
        "Body Control",
        "Climb",
        "Covert Movement",
        "Dance",
        "Distance Running",
        "Drive",
        "Endurance",
        "Escape Artist",
        "Grace",
        "Gymnastics",
        "Inconspicuous",
        "Pilot (Groundcar)",
        "Pilot (Ornithopter)",
        "Pilot (Spacecraft)",
        "Running",
        "Sleight of Hand",
        "Stamina",
        "Stealth",
        "Swimming",
        "Unobtrusive",
    ],
    SkillName.UNDERSTAND: [
        "Advanced Technology",
        "Astronomy",
        "Biology",
        "Body Language",
        "Botany",
        "CHOAM Bureaucracy",
        "Combat Awareness",
        "Cryptography",
        "Cultural Studies",
        "Danger Sense",
        "Data Analysis",
        "Deductive Reasoning",
        "Ecology",
        "Economics",
        "Heraldry",
        "History",
        "Holtzman Fields",
        "Imperial Law",
        "Kanly",
        "Medicine",
        "Philosophy",
        "Poisons",
        "Politics",
        "Psychology",
        "Science",
        "Sietch Customs",
        "Social Awareness",
        "Strategy",
        "Technology",
        "Treaties",
        "Warfare",
    ],
}


def get_all_focuses() -> List[str]:
    """Return a flat sorted list of unique standard focuses."""
    all_f = set()
    for focuses in STANDARD_FOCUSES.values():
        all_f.update(focuses)
    return sorted(list(all_f))
