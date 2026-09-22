"""Canonical Archetypes from Dune: Adventures in the Imperium core rules (p. 113-125)."""

from dataclasses import dataclass
from typing import Dict, List, Optional
from dune_char_gen.models.enums import SkillName


@dataclass(frozen=True)
class ArchetypeDefinition:
    name: str
    primary_skill: SkillName
    secondary_skill: SkillName
    suggested_focuses: List[str]
    suggested_talent: str
    description: str
    drive_advice: str


ARCHETYPES: Dict[str, ArchetypeDefinition] = {
    "Duelist": ArchetypeDefinition(
        name="Duelist",
        primary_skill=SkillName.BATTLE,
        secondary_skill=SkillName.MOVE,
        suggested_focuses=["Dueling", "Short Blades"],
        suggested_talent="The Slow Blade",
        description="Mastery of the blade is a prized skill in the Imperium. Champions, favored gladiators, and bodyguard tutors.",
        drive_advice="Believers that might makes right, feeling Justice is enacted by the blade or Power is proven in single combat.",
    ),
    "Sergeant": ArchetypeDefinition(
        name="Sergeant",
        primary_skill=SkillName.BATTLE,
        secondary_skill=SkillName.COMMUNICATE,
        suggested_focuses=["Long Blades", "Strategy"],
        suggested_talent="Master-at-Arms",
        description="Experienced combat leaders who command soldiers in the field, drill house guards, and lead tactical squads.",
        drive_advice="Duty and loyalty to the House and their unit; pride in hard discipline.",
    ),
    "Tactician": ArchetypeDefinition(
        name="Tactician",
        primary_skill=SkillName.BATTLE,
        secondary_skill=SkillName.UNDERSTAND,
        suggested_focuses=["Combat Awareness", "Tactics"],
        suggested_talent="Decisive Action",
        description="Planners of skirmishes and wars, reading the battlefield like a chessboard and anticipating enemy moves.",
        drive_advice="Truth of battle calculus and Power through decisive positioning.",
    ),
    "Warrior": ArchetypeDefinition(
        name="Warrior",
        primary_skill=SkillName.BATTLE,
        secondary_skill=SkillName.DISCIPLINE,
        suggested_focuses=["Dirty Fighting", "Long Blades"],
        suggested_talent="To Fight Someone Is to Know Them",
        description="Grit-tested frontline combatants, veteran shock troopers, and steadfast defenders of their House.",
        drive_advice="Faith in their training, Duty to their comrades, or relentless pursuit of Justice.",
    ),
    "Commander": ArchetypeDefinition(
        name="Commander",
        primary_skill=SkillName.COMMUNICATE,
        secondary_skill=SkillName.BATTLE,
        suggested_focuses=["Inspiration", "Leadership"],
        suggested_talent="Specialist (Warfare Assets)",
        description="Inspirational commanders, generals, and leaders who direct grand endeavors and inspire loyalty under fire.",
        drive_advice="Power over armies, Duty to the noble banner, and unwavering Faith in ultimate victory.",
    ),
    "Courtier": ArchetypeDefinition(
        name="Courtier",
        primary_skill=SkillName.COMMUNICATE,
        secondary_skill=SkillName.UNDERSTAND,
        suggested_focuses=["Charm", "Musical Instrument"],
        suggested_talent="Subtle Words",
        description="Charming aristocrats, socialites, entertainers, and salon manipulators adept in Imperial etiquette and kanly.",
        drive_advice="Power wielded in drawing rooms, uncovering the hidden Truth of court secrets.",
    ),
    "Envoy": ArchetypeDefinition(
        name="Envoy",
        primary_skill=SkillName.COMMUNICATE,
        secondary_skill=SkillName.MOVE,
        suggested_focuses=["Diplomacy", "Persuasion"],
        suggested_talent="Binding Promise",
        description="Diplomats, ambassadors, negotiators, and arbitrators sent across worlds to forge treaties and settle disputes.",
        drive_advice="Duty to the realm, Justice in diplomacy, and the delicate balance of Power.",
    ),
    "Steward": ArchetypeDefinition(
        name="Steward",
        primary_skill=SkillName.COMMUNICATE,
        secondary_skill=SkillName.DISCIPLINE,
        suggested_focuses=["Leadership", "Negotiation"],
        suggested_talent="Stirring Rhetoric",
        description="Governors, treasurers, and major-domos managing territories, logistics, and personnel with firm dignity.",
        drive_advice="Devotion to Duty and the orderly execution of justice and administrative Power.",
    ),
    "Analyst": ArchetypeDefinition(
        name="Analyst",
        primary_skill=SkillName.DISCIPLINE,
        secondary_skill=SkillName.UNDERSTAND,
        suggested_focuses=["Attention to Detail", "Composure"],
        suggested_talent="Intense Study",
        description="Methodical minds who filter signal from noise, evaluate risks, and sift intelligence with serene composure.",
        drive_advice="Pure Truth through verification and quiet Duty to their superiors.",
    ),
    "Herald": ArchetypeDefinition(
        name="Herald",
        primary_skill=SkillName.DISCIPLINE,
        secondary_skill=SkillName.COMMUNICATE,
        suggested_focuses=["Command", "Composure"],
        suggested_talent="Rigorous Control",
        description="The formal voice of a House, delivering proclamations, presiding over rituals, and enforcing protocol.",
        drive_advice="Unyielding Duty to ancestral rank, Faith in ancient tradition and Imperial order.",
    ),
    "Infiltrator": ArchetypeDefinition(
        name="Infiltrator",
        primary_skill=SkillName.DISCIPLINE,
        secondary_skill=SkillName.MOVE,
        suggested_focuses=["Infiltration", "Precision"],
        suggested_talent="Subtle Step",
        description="Ghosts and covert operatives who slip past perimeter shields, pick locks, and plant surveillance devices.",
        drive_advice="Duty to the shadows, or Justice delivered where open law cannot reach.",
    ),
    "Protector": ArchetypeDefinition(
        name="Protector",
        primary_skill=SkillName.DISCIPLINE,
        secondary_skill=SkillName.BATTLE,
        suggested_focuses=["Resolve", "Self-Control"],
        suggested_talent="Bolster",
        description="Steadfast bodyguards and personal shields willing to intercept assassination attempts and poisoned blades.",
        drive_advice="Absolute Duty to their charge and Faith in their shield and oath.",
    ),
    "Athlete": ArchetypeDefinition(
        name="Athlete",
        primary_skill=SkillName.MOVE,
        secondary_skill=SkillName.DISCIPLINE,
        suggested_focuses=["Grace", "Stamina"],
        suggested_talent="Nimble",
        description="Acrobats, runners, gymnasts, and physical paragons pushing the limits of the human body through intense conditioning.",
        drive_advice="Faith in biological perfection, Power forged through physical supremacy.",
    ),
    "Messenger": ArchetypeDefinition(
        name="Messenger",
        primary_skill=SkillName.MOVE,
        secondary_skill=SkillName.COMMUNICATE,
        suggested_focuses=["Pilot (Ornithopter)", "Unobtrusive"],
        suggested_talent="Masterful Innuendo",
        description="Couriers, dispatch pilots, and secret messengers who carry vital communications between distant holdings.",
        drive_advice="Duty to deliver the dispatch at all costs; Truth preserved in transit.",
    ),
    "Scout": ArchetypeDefinition(
        name="Scout",
        primary_skill=SkillName.MOVE,
        secondary_skill=SkillName.UNDERSTAND,
        suggested_focuses=["Endurance", "Stealth"],
        suggested_talent="Putting Theory into Practice",
        description="Pathfinders, wilderness guides, and planetary survey specialists exploring uncharted dunes and harsh frontiers.",
        drive_advice="Truth found in nature, Faith in survival instincts, and Duty to guide their companions.",
    ),
    "Smuggler": ArchetypeDefinition(
        name="Smuggler",
        primary_skill=SkillName.MOVE,
        secondary_skill=SkillName.BATTLE,
        suggested_focuses=["Pilot (Spacecraft)", "Unobtrusive"],
        suggested_talent="Subtle Step",
        description="Shadow traders, blockade runners, and black-market pilots operating under the nose of CHOAM and Guild authorities.",
        drive_advice="Personal Power, defiance of unjust laws (Justice), or practical survival.",
    ),
    "Empath": ArchetypeDefinition(
        name="Empath",
        primary_skill=SkillName.UNDERSTAND,
        secondary_skill=SkillName.COMMUNICATE,
        suggested_focuses=["Body Language", "Social Awareness"],
        suggested_talent="Passive Scrutiny",
        description="Keen observers of human emotion, voice inflection, and micro-expressions, sensing deceit and hidden intent.",
        drive_advice="Relentless pursuit of Truth and deep understanding of human vulnerability and Power.",
    ),
    "Scholar": ArchetypeDefinition(
        name="Scholar",
        primary_skill=SkillName.UNDERSTAND,
        secondary_skill=SkillName.DISCIPLINE,
        suggested_focuses=["Data Analysis", "Deductive Reasoning"],
        suggested_talent="Intense Study",
        description="Archivists, historians, philosophers, and scientists preserving humanity's vast post-Jihad knowledge.",
        drive_advice="Reverence for Truth, philosophical Faith, and duty to enlightenment.",
    ),
    "Spy": ArchetypeDefinition(
        name="Spy",
        primary_skill=SkillName.UNDERSTAND,
        secondary_skill=SkillName.MOVE,
        suggested_focuses=["Deductive Reasoning", "Kanly"],
        suggested_talent="Hidden Motives",
        description="Secret agents, spymasters, and handlers orchestrating clandestine operations and kanly vendettas.",
        drive_advice="Truth extracted from rivals, Power gained through black intelligence.",
    ),
    "Strategist": ArchetypeDefinition(
        name="Strategist",
        primary_skill=SkillName.UNDERSTAND,
        secondary_skill=SkillName.BATTLE,
        suggested_focuses=["Kanly", "Strategy"],
        suggested_talent="Master-at-Arms",
        description="Grand planners of campaigns, political wars of assassins, and economic siegecraft across planetary scales.",
        drive_advice="Mastery of Power through foresight and adherence to the Truth of numbers and logistics.",
    ),
}


def get_archetype(name: str) -> Optional[ArchetypeDefinition]:
    return ARCHETYPES.get(name)


def get_all_archetype_names() -> List[str]:
    return sorted(list(ARCHETYPES.keys()))
