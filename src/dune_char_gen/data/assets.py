"""Assets catalog from Dune: Adventures in the Imperium (p. 198-225)."""

from dataclasses import dataclass
from typing import Dict, List, Optional
from dune_char_gen.models.enums import AssetType


@dataclass(frozen=True)
class AssetDefinition:
    name: str
    asset_type: AssetType
    category: str
    quality: int
    traits: List[str]
    description: str


ASSETS: Dict[str, AssetDefinition] = {
    # Tangible: Weapons
    "Kindjal": AssetDefinition(
        name="Kindjal",
        asset_type=AssetType.TANGIBLE,
        category="Personal Weapons",
        quality=0,
        traits=["Blade", "Melee", "Concealed"],
        description="A traditional double-edged long dagger favored by nobility and duelists.",
    ),
    "Crysknife": AssetDefinition(
        name="Crysknife",
        asset_type=AssetType.TANGIBLE,
        category="Personal Weapons",
        quality=1,
        traits=["Sacred", "Blade", "Deadly", "Unfixed"],
        description="Carved from the tooth of Shai-Hulud; never to be sheathed without drawing blood.",
    ),
    "Blade": AssetDefinition(
        name="Blade",
        asset_type=AssetType.TANGIBLE,
        category="Personal Weapons",
        quality=0,
        traits=["Blade", "Melee"],
        description="A standard sword or combat knife used throughout the Imperium.",
    ),
    "Bodkin": AssetDefinition(
        name="Bodkin",
        asset_type=AssetType.TANGIBLE,
        category="Personal Weapons",
        quality=0,
        traits=["Blade", "Piercing", "Concealed"],
        description="A thin, needle-pointed dagger crafted to bypass armor seams or slide through shields slowly.",
    ),
    "Pulse-Sword": AssetDefinition(
        name="Pulse-Sword",
        asset_type=AssetType.TANGIBLE,
        category="Personal Weapons",
        quality=1,
        traits=["Vibrating", "High-Tech", "Deadly"],
        description="A high-frequency vibrating blade capable of shearing through tough alloys.",
    ),
    "Maula Pistol": AssetDefinition(
        name="Maula Pistol",
        asset_type=AssetType.TANGIBLE,
        category="Ranged Weapons",
        quality=0,
        traits=["Ranged", "Spring-Loaded", "Silent"],
        description="A spring-loaded dart pistol throwing poison or tranquilizer needles silently.",
    ),
    "Lasgun": AssetDefinition(
        name="Lasgun",
        asset_type=AssetType.TANGIBLE,
        category="Ranged Weapons",
        quality=1,
        traits=["Energy", "Continuous Beam", "Extreme Range", "Volatile vs Shields"],
        description="A continuous-wave laser carbine. Catastrophic Holtzman sub-atomic explosion if fired at a shield!",
    ),
    "Dartgun": AssetDefinition(
        name="Dartgun",
        asset_type=AssetType.TANGIBLE,
        category="Ranged Weapons",
        quality=0,
        traits=["Concealed", "Silent", "Poison-Delivery"],
        description="A palm-sized or forearm-mounted projectile weapon firing lethal slips or paralytics.",
    ),
    "Hunter-Seeker": AssetDefinition(
        name="Hunter-Seeker",
        asset_type=AssetType.TANGIBLE,
        category="Assassination Gear",
        quality=1,
        traits=["Suspensor", "Autonomous", "Lethal Needle", "Requires Line-of-Sight Operator"],
        description="A compressed sliver of metal suspended on an anti-gravity field, steered by an assassin's eye.",
    ),
    "Slip-Tip": AssetDefinition(
        name="Slip-Tip",
        asset_type=AssetType.TANGIBLE,
        category="Assassination Gear",
        quality=0,
        traits=["Coated Blade", "Poison"],
        description="A knife treated with lethal chaumurky or chaumas residue on a quick-release blade sheath.",
    ),

    # Tangible: Protective Gear
    "Personal Shield": AssetDefinition(
        name="Personal Shield",
        asset_type=AssetType.TANGIBLE,
        category="Defenses",
        quality=0,
        traits=["Holtzman Field", "Kinetic Deflector", "Energy Barrier"],
        description="A waist-worn Holtzman generator enveloping the wearer in a shimmering protective field that stops fast velocity.",
    ),
    "Stillsuit": AssetDefinition(
        name="Stillsuit",
        asset_type=AssetType.TANGIBLE,
        category="Survival Gear",
        quality=1,
        traits=["Water-Reclamation", "Thermal Regulation", "Desert Essential"],
        description="Micro-sandwich filtration suit capturing all bodily moisture and recycling it to pure drinkable water.",
    ),
    "Jubba Cloak": AssetDefinition(
        name="Jubba Cloak",
        asset_type=AssetType.TANGIBLE,
        category="Survival Gear",
        quality=0,
        traits=["Thermal Cloak", "Camouflage"],
        description="An all-weather desert robe worn over stillsuits to deflect searing sun and harsh sandstorms.",
    ),

    # Tangible: Tools & Devices
    "Poison Snooper": AssetDefinition(
        name="Poison Snooper",
        asset_type=AssetType.TANGIBLE,
        category="Sensors & Security",
        quality=0,
        traits=["Olfactory Scanner", "Chemical Analysis"],
        description="An olfactory sensor tuned to detect hundreds of volatile poisons and toxins in food or air.",
    ),
    "Fremkit": AssetDefinition(
        name="Fremkit",
        asset_type=AssetType.TANGIBLE,
        category="Survival Gear",
        quality=0,
        traits=["Desert Kit", "Tools"],
        description="Standard Arrakeen survival kit containing maker hooks, thumper, filter straws, sand-compass, and beacons.",
    ),
    "Personal Suspensor": AssetDefinition(
        name="Personal Suspensor",
        asset_type=AssetType.TANGIBLE,
        category="Mobility",
        quality=0,
        traits=["Anti-Gravity", "Null-G", "Quiet"],
        description="Holtzman field harness that reduces the wearer's effective mass for gliding and silent falls.",
    ),
    "Filmbook & Reader": AssetDefinition(
        name="Filmbook & Reader",
        asset_type=AssetType.TANGIBLE,
        category="Scholarship & Intelligence",
        quality=0,
        traits=["Archive", "Mnemonic", "Encrypted"],
        description="A shigawire-imprinted informational tome containing comprehensive archives of history, law, or fauna.",
    ),
    "Sapho Juice": AssetDefinition(
        name="Sapho Juice",
        asset_type=AssetType.TANGIBLE,
        category="Consumables",
        quality=0,
        traits=["Cognitive Booster", "Mentat Tool"],
        description="Extracted from Ecaz tree roots, boiling mental energy to extraordinary heights and staining lips ruby red.",
    ),
    "Ixian Damper": AssetDefinition(
        name="Ixian Damper",
        asset_type=AssetType.TANGIBLE,
        category="Espionage Gear",
        quality=1,
        traits=["Sound Suppression", "Surveillance Blocker"],
        description="A compact generator projecting a distortion cone that muffles sound and conceals conversation.",
    ),

    # Intangible: Contacts, Favors & Standing
    "House Retainer Contract": AssetDefinition(
        name="House Retainer Contract",
        asset_type=AssetType.INTANGIBLE,
        category="Status & Affiliation",
        quality=0,
        traits=["Fealty", "House Protection", "Stipend"],
        description="Official patent of service granting legal authority, livery privileges, and House backing.",
    ),
    "Old Friendship": AssetDefinition(
        name="Old Friendship",
        asset_type=AssetType.INTANGIBLE,
        category="Social Ties",
        quality=0,
        traits=["Trust", "Reliable", "Personal Bond"],
        description="A longstanding comrade, veteran squadmate, or court ally willing to grant sanctuary or favors.",
    ),
    "Significant Favor Owed": AssetDefinition(
        name="Significant Favor Owed",
        asset_type=AssetType.INTANGIBLE,
        category="Leverage",
        quality=1,
        traits=["Leverage", "One-Time Call", "High-Value"],
        description="A blood debt or political marker owed by an influential noble, merchant lord, or guild officer.",
    ),
    "Network of Informants": AssetDefinition(
        name="Network of Informants",
        asset_type=AssetType.INTANGIBLE,
        category="Espionage & Secrets",
        quality=1,
        traits=["Covert", "Eavesdropping", "Whisperers"],
        description="A reliable circle of servants, dockworkers, or low-ranking clerks passing rumors and movements.",
    ),
    "Blackmail Dossier": AssetDefinition(
        name="Blackmail Dossier",
        asset_type=AssetType.INTANGIBLE,
        category="Leverage",
        quality=1,
        traits=["Secret", "Damning", "Kanly Weapon"],
        description="Irrefutable evidence of financial embezzlement, illicit tech, or treason against a rival rival House.",
    ),
    "CHOAM Trading Permit": AssetDefinition(
        name="CHOAM Trading Permit",
        asset_type=AssetType.INTANGIBLE,
        category="Economic Influence",
        quality=0,
        traits=["Monopoly", "Commerce", "Customs Immunity"],
        description="Official authorization to barter, freight, and trade restricted commodities across star systems.",
    ),
    "Smuggler Safehouse Access": AssetDefinition(
        name="Smuggler Safehouse Access",
        asset_type=AssetType.INTANGIBLE,
        category="Criminal Contacts",
        quality=0,
        traits=["Underworld", "Shelter", "Off-Grid"],
        description="Code words and clearances granting refuge, unmarked transport, and black market access.",
    ),
    "Noble Title / Scion Standing": AssetDefinition(
        name="Noble Title / Scion Standing",
        asset_type=AssetType.INTANGIBLE,
        category="Status & Affiliation",
        quality=1,
        traits=["Aristocratic", "Landsraad Privileges", "Diplomatic Immunity"],
        description="Recognized aristocratic lineage granting audience rights, precedence in duels, and formal deference.",
    ),
    "Mentat Master of Assassins Network": AssetDefinition(
        name="Mentat Master of Assassins Network",
        asset_type=AssetType.INTANGIBLE,
        category="Espionage & Secrets",
        quality=1,
        traits=["Lethal", "Calculated", "Covert"],
        description="Access to coded assassination dead-drops and specialized poisoners trained in kanly protocol.",
    ),
}


def get_asset(name: str) -> Optional[AssetDefinition]:
    return ASSETS.get(name)


def get_all_asset_names(asset_type: Optional[AssetType] = None) -> List[str]:
    if asset_type is None:
        return sorted(list(ASSETS.keys()))
    return sorted([k for k, v in ASSETS.items() if v.asset_type == asset_type])
