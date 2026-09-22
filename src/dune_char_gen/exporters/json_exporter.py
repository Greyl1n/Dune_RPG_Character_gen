"""JSON exporter and loader for Dune characters."""

import json
from pathlib import Path
from typing import Union
from dune_char_gen.models.character import Character


def character_to_json(character: Character, indent: int = 2) -> str:
    """Serialize a Character object to a JSON string."""
    return json.dumps(character.to_dict(), indent=indent, ensure_ascii=False)


def character_from_json(json_str: str) -> Character:
    """Deserialize a Character object from a JSON string."""
    data = json.loads(json_str)
    return Character.from_dict(data)


def save_character_to_file(character: Character, file_path: Union[str, Path]) -> None:
    """Save character to a JSON file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(character_to_json(character))


def load_character_from_file(file_path: Union[str, Path]) -> Character:
    """Load character from a JSON file."""
    path = Path(file_path)
    with open(path, "r", encoding="utf-8") as f:
        return character_from_json(f.read())
