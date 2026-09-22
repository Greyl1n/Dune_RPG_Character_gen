"""Faction templates from Dune: Adventures in the Imperium (p. 110-112)."""

from dataclasses import dataclass
from typing import Dict, List, Optional
from dune_char_gen.models.enums import FactionType


@dataclass(frozen=True)
class FactionTemplate:
    faction_type: FactionType
    name: str
    additional_trait: str
    mandatory_talents: List[str]
    # If True, player must select ALL mandatory talents; if False, player selects at least one from the list
    require_all_mandatory: bool
    suggested_archetypes: List[str]
    description: str


FACTION_TEMPLATES: Dict[FactionType, FactionTemplate] = {
    FactionType.NONE: FactionTemplate(
        faction_type=FactionType.NONE,
        name="None (House Retainer / Independent)",
        additional_trait="",
        mandatory_talents=[],
        require_all_mandatory=False,
        suggested_archetypes=[],
        description="A loyal agent, retainer, courtier, officer, or noble scion of the House without allegiance to an external faction.",
    ),
    FactionType.BENE_GESSERIT: FactionTemplate(
        faction_type=FactionType.BENE_GESSERIT,
        name="Bene Gesserit Sister",
        additional_trait="Bene Gesserit",
        mandatory_talents=["Prana-bindu Conditioning"],
        require_all_mandatory=True,
        suggested_archetypes=[
            "Analyst",
            "Athlete",
            "Courtier",
            "Empath",
            "Envoy",
            "Infiltrator",
            "Protector",
            "Scholar",
            "Spy",
            "Warrior",
        ],
        description=(
            "Trained in the secretive Sisterhood of the Bene Gesserit. Possesses unmatched bodily control, "
            "vocal command (the Voice), perceptive acumen, and loyalty divided between House and the Sisterhood."
        ),
    ),
    FactionType.FREMEN: FactionTemplate(
        faction_type=FactionType.FREMEN,
        name="Fremen",
        additional_trait="Fremen",
        mandatory_talents=[
            "Dedication",
            "Driven",
            "Master-at-Arms",
            "Rapid Recovery",
            "Resilience",
            "Subtle Step",
            "The Reason I Fight",
        ],
        require_all_mandatory=False,  # Pick at least one from the list
        suggested_archetypes=[
            "Athlete",
            "Duelist",
            "Infiltrator",
            "Protector",
            "Scout",
            "Sergeant",
            "Warrior",
        ],
        description=(
            "Desert warriors of Arrakis, hardened by extreme dune ecology and bonded by sietch water-discipline. "
            "Fierce, direct, and unshakeable in faith and tribal bonds."
        ),
    ),
    FactionType.MENTAT: FactionTemplate(
        faction_type=FactionType.MENTAT,
        name="Mentat",
        additional_trait="Mentat",
        mandatory_talents=[
            "Calculated Prediction",
            "Mentat Discipline",
            "Mind Palace",
            "Twisted Mentat",
            "Verify",
        ],
        require_all_mandatory=False,  # Pick at least one from the list
        suggested_archetypes=[
            "Analyst",
            "Empath",
            "Envoy",
            "Herald",
            "Scholar",
            "Spy",
            "Steward",
            "Strategist",
            "Tactician",
        ],
        description=(
            "Human computers trained to process vast flows of data and probability following the Butlerian Jihad's "
            "proscription of thinking machines. Indispensable strategic and administrative advisors to noble Houses."
        ),
    ),
    FactionType.SPACING_GUILD: FactionTemplate(
        faction_type=FactionType.SPACING_GUILD,
        name="Spacing Guild Agent",
        additional_trait="Guild Agent",
        mandatory_talents=["Guildsman"],
        require_all_mandatory=True,
        suggested_archetypes=[
            "Analyst",
            "Courtier",
            "Envoy",
            "Messenger",
            "Scholar",
            "Scout",
            "Smuggler",
            "Spy",
            "Strategist",
        ],
        description=(
            "Emissary or factor of the Spacing Guild, the interstellar monopoly holding absolute sway over foldspace "
            "travel and banking. Pragmatic, calculating, and protective of Guild transport privileges."
        ),
    ),
    FactionType.SUK_DOCTOR: FactionTemplate(
        faction_type=FactionType.SUK_DOCTOR,
        name="Suk Doctor",
        additional_trait="Suk Doctor",
        mandatory_talents=["Imperial Conditioning"],
        require_all_mandatory=True,
        suggested_archetypes=[
            "Analyst",
            "Commander",
            "Courtier",
            "Herald",
            "Scholar",
            "Steward",
        ],
        description=(
            "Graduate of the Suk Inner School of Medicine bearing the diamond tattoo of Imperial Conditioning. "
            "Reputedly incapable of taking human life, they are the most trusted physicians in the Imperium."
        ),
    ),
}


def get_faction_template(faction_type: FactionType) -> FactionTemplate:
    return FACTION_TEMPLATES[faction_type]
