from enum import Enum


class SkillName(str, Enum):
    BATTLE = "Battle"
    COMMUNICATE = "Communicate"
    DISCIPLINE = "Discipline"
    MOVE = "Move"
    UNDERSTAND = "Understand"


class DriveName(str, Enum):
    DUTY = "Duty"
    FAITH = "Faith"
    JUSTICE = "Justice"
    POWER = "Power"
    TRUTH = "Truth"


class FactionType(str, Enum):
    NONE = "None (House Retainer / Independent)"
    BENE_GESSERIT = "Bene Gesserit Sister"
    FREMEN = "Fremen"
    MENTAT = "Mentat"
    SPACING_GUILD = "Spacing Guild Agent"
    SUK_DOCTOR = "Suk Doctor"


class AssetType(str, Enum):
    TANGIBLE = "Tangible"
    INTANGIBLE = "Intangible"


class CharacterType(str, Enum):
    PLAYER_CHARACTER = "Player Character"
    NOTABLE_NPC = "Notable Supporting Character"
    MINOR_NPC = "Minor Supporting Character"
