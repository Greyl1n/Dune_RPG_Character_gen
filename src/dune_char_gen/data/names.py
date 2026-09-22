"""Name generation tables tailored for Dune lore."""

import random
from typing import Optional
from dune_char_gen.models.enums import FactionType

IMPERIAL_FIRST_NAMES = [
    "Leto", "Paul", "Victor", "Paulus", "Dominic", "Rhombur", "Iakin", "Hasimir",
    "Shaddam", "Morzan", "Cammar", "Yorek", "Vladimir", "Feyd", "Glossu", "Abulurd",
    "Gurney", "Duncan", "Thufir", "Piter", "Wellington", "Whitmore", "Josef",
    "Jessica", "Irulan", "Chani", "Margot", "Helena", "Wensicia", "Kailea",
    "Lucilla", "Darwi", "Miles", "Tylwyth", "Gaius", "Anirul", "Chalice", "Serena"
]

IMPERIAL_SURNAMES = [
    "Atreides", "Harkonnen", "Corrino", "Moritani", "Vernius", "Richese", "Ecaz",
    "Fenring", "Ginaz", "Molay", "Kenric", "Taligari", "Thorvald", "Bular", "Nefud",
    "Rabban", "Hawat", "Halleck", "Idaho", "De Vries", "Yueh", "Blond", "Kadur"
]

FREMEN_FIRST_NAMES = [
    "Stilgar", "Jamis", "Liet", "Pardot", "Chani", "Harah", "Shadout", "Mapes",
    "Farok", "Otheym", "Korba", "Shimay", "Geoff", "Jahid", "Barkan", "Assan",
    "Kastur", "Taneg", "Daryal", "El-Nur", "Ziam", "Mura", "Sabiha", "Tirza"
]

FREMEN_SIETCH_NAMES = [
    "Tabr", "Chin Rock", "Clave", "Red Chasm", "Tuono", "Bight", "Jacurutu",
    "Sihaya", "Carthag Outskirts", "Gara Kulon", "Habbanya", "Tirzah"
]

TITLES_BY_FACTION = {
    FactionType.BENE_GESSERIT: ["Sister", "Adept", "Mother", "Reverend Mother", "Truthsayer"],
    FactionType.MENTAT: ["Mentat", "Master Mentat", "Computational Advisor", "Archivist"],
    FactionType.SPACING_GUILD: ["Agent", "Factor", "Plenipotentiary", "Auditor"],
    FactionType.SUK_DOCTOR: ["Doctor", "Chief Physician", "Imperial Suk", "Healer"],
    FactionType.FREMEN: ["Naib", "Fedaykin", "Sandrider", "Water-Master", "Scout"],
    FactionType.NONE: ["Lord", "Lady", "Captain", "Master", "Commander", "Sir", "Counselor"]
}


def generate_dune_name(faction: Optional[FactionType] = None) -> str:
    """Generate a lore-appropriate Dune character name."""
    if faction == FactionType.FREMEN:
        first = random.choice(FREMEN_FIRST_NAMES)
        sietch = random.choice(FREMEN_SIETCH_NAMES)
        if random.random() < 0.4:
            return f"{first} of Sietch {sietch}"
        return f"{first}"
    
    first = random.choice(IMPERIAL_FIRST_NAMES)
    surname = random.choice(IMPERIAL_SURNAMES)
    return f"{first} {surname}"
