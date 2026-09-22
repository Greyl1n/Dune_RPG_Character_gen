"""Character domain models for Dune: Adventures in the Imperium."""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from dune_char_gen.models.enums import SkillName, DriveName, FactionType, AssetType, CharacterType


@dataclass
class FocusItem:
    name: str
    skill: SkillName

    def to_dict(self) -> dict:
        return {"name": self.name, "skill": self.skill.value}

    @classmethod
    def from_dict(cls, data: dict) -> "FocusItem":
        return cls(name=data["name"], skill=SkillName(data["skill"]))


@dataclass
class TalentItem:
    name: str
    specialization: Optional[str] = None
    description: str = ""

    @property
    def display_name(self) -> str:
        if self.specialization:
            return f"{self.name} ({self.specialization})"
        return self.name

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "specialization": self.specialization,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TalentItem":
        return cls(
            name=data["name"],
            specialization=data.get("specialization"),
            description=data.get("description", ""),
        )


@dataclass
class AssetItem:
    name: str
    asset_type: AssetType
    quality: int = 0
    traits: List[str] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "asset_type": self.asset_type.value,
            "quality": self.quality,
            "traits": self.traits,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AssetItem":
        return cls(
            name=data["name"],
            asset_type=AssetType(data["asset_type"]),
            quality=data.get("quality", 0),
            traits=data.get("traits", []),
            description=data.get("description", ""),
        )


@dataclass
class Character:
    # Metadata & Concept
    name: str = "New Character"
    player_name: str = ""
    concept: str = ""
    character_type: CharacterType = CharacterType.PLAYER_CHARACTER
    
    # Allegiances
    house: str = "House Atreides"
    homeworld: str = "Caladan"
    house_role: str = "Retainer"
    house_trait: str = ""
    
    # Faction & Archetype
    faction: FactionType = FactionType.NONE
    faction_trait: str = ""
    archetype: str = "Warrior"
    archetype_trait: str = "Warrior"
    personal_trait: str = "Disciplined"
    
    # Skills (Rating 4 to 8, base sum 28 for PC)
    skills: Dict[SkillName, int] = field(default_factory=lambda: {
        SkillName.BATTLE: 6,
        SkillName.COMMUNICATE: 5,
        SkillName.DISCIPLINE: 6,
        SkillName.MOVE: 6,
        SkillName.UNDERSTAND: 5,
    })
    
    # Focuses (4 for PC, at least 1 for primary skill)
    focuses: List[FocusItem] = field(default_factory=list)
    
    # Drives (Ratings 4, 5, 6, 7, 8)
    drives: Dict[DriveName, int] = field(default_factory=lambda: {
        DriveName.DUTY: 8,
        DriveName.FAITH: 5,
        DriveName.JUSTICE: 7,
        DriveName.POWER: 6,
        DriveName.TRUTH: 4,
    })
    
    # Drive Statements (Assigned to top 3 drives: 8, 7, 6)
    drive_statements: Dict[DriveName, str] = field(default_factory=dict)
    
    # Ambition & Determination
    ambition: str = ""
    determination: int = 1
    
    # Talents (3 for PC, including mandatory faction talents)
    talents: List[TalentItem] = field(default_factory=list)
    
    # Assets (3 for PC, at least 1 tangible)
    assets: List[AssetItem] = field(default_factory=list)
    
    # Personal details
    appearance: str = ""
    personality: str = ""
    relationships: str = ""
    notes: str = ""

    @property
    def all_traits(self) -> List[str]:
        traits = []
        if self.personal_trait:
            traits.append(self.personal_trait)
        if self.archetype_trait:
            traits.append(self.archetype_trait)
        if self.faction_trait:
            traits.append(self.faction_trait)
        if self.house_trait:
            traits.append(self.house_trait)
        return traits

    def get_skill(self, skill: SkillName) -> int:
        return self.skills.get(skill, 4)

    def set_skill(self, skill: SkillName, value: int) -> None:
        self.skills[skill] = value

    def get_drive(self, drive: DriveName) -> int:
        return self.drives.get(drive, 4)

    def set_drive(self, drive: DriveName, value: int) -> None:
        self.drives[drive] = value

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "player_name": self.player_name,
            "concept": self.concept,
            "character_type": self.character_type.value,
            "house": self.house,
            "homeworld": self.homeworld,
            "house_role": self.house_role,
            "house_trait": self.house_trait,
            "faction": self.faction.value,
            "faction_trait": self.faction_trait,
            "archetype": self.archetype,
            "archetype_trait": self.archetype_trait,
            "personal_trait": self.personal_trait,
            "skills": {k.value: v for k, v in self.skills.items()},
            "focuses": [f.to_dict() for f in self.focuses],
            "drives": {k.value: v for k, v in self.drives.items()},
            "drive_statements": {k.value: v for k, v in self.drive_statements.items()},
            "ambition": self.ambition,
            "determination": self.determination,
            "talents": [t.to_dict() for t in self.talents],
            "assets": [a.to_dict() for a in self.assets],
            "appearance": self.appearance,
            "personality": self.personality,
            "relationships": self.relationships,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Character":
        char = cls(
            name=data.get("name", "Unnamed"),
            player_name=data.get("player_name", ""),
            concept=data.get("concept", ""),
            character_type=CharacterType(data.get("character_type", CharacterType.PLAYER_CHARACTER.value)),
            house=data.get("house", "House Atreides"),
            homeworld=data.get("homeworld", "Caladan"),
            house_role=data.get("house_role", "Retainer"),
            house_trait=data.get("house_trait", ""),
            faction=FactionType(data.get("faction", FactionType.NONE.value)),
            faction_trait=data.get("faction_trait", ""),
            archetype=data.get("archetype", "Warrior"),
            archetype_trait=data.get("archetype_trait", "Warrior"),
            personal_trait=data.get("personal_trait", "Disciplined"),
            skills={SkillName(k): v for k, v in data.get("skills", {}).items()},
            focuses=[FocusItem.from_dict(f) for f in data.get("focuses", [])],
            drives={DriveName(k): v for k, v in data.get("drives", {}).items()},
            drive_statements={DriveName(k): v for k, v in data.get("drive_statements", {}).items()},
            ambition=data.get("ambition", ""),
            determination=data.get("determination", 1),
            talents=[TalentItem.from_dict(t) for t in data.get("talents", [])],
            assets=[AssetItem.from_dict(a) for a in data.get("assets", [])],
            appearance=data.get("appearance", ""),
            personality=data.get("personality", ""),
            relationships=data.get("relationships", ""),
            notes=data.get("notes", ""),
        )
        return char
