"""Rich-powered CLI for Dune: Adventures in the Imperium character generator."""

import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from dune_char_gen.models.enums import FactionType, AssetType, CharacterType
from dune_char_gen.generators.random_generator import generate_random_character
from dune_char_gen.generators.npc_generator import generate_minor_npc, generate_notable_npc
from dune_char_gen.models.validation import validate_character
from dune_char_gen.exporters.json_exporter import character_to_json, load_character_from_file, save_character_to_file
from dune_char_gen.exporters.markdown_exporter import character_to_markdown
from dune_char_gen.exporters.html_exporter import character_to_html
from dune_char_gen.models.character import Character

console = Console()


def print_character_summary(char: Character) -> None:
    """Print a styled terminal summary of the character."""
    title_text = Text()
    title_text.append(f"{char.name}\n", style="bold gold1")
    title_text.append(f"{char.concept}\n\n", style="italic")
    title_text.append(f"House: {char.house} ({char.homeworld}) | Role: {char.house_role}\n", style="cyan")
    if char.faction != FactionType.NONE:
        title_text.append(f"Faction: {char.faction.value} | ", style="magenta")
    title_text.append(f"Archetype: {char.archetype}\n", style="yellow")
    title_text.append(f"Traits: {', '.join(char.all_traits)} | Determination: {char.determination}", style="green")

    console.print(Panel(title_text, title="DUNE: ADVENTURES IN THE IMPERIUM", border_style="gold1"))

    # Ambition
    if char.ambition:
        console.print(Panel(f"[bold italic]{char.ambition}[/]", title="Ambition", border_style="red"))

    # Two tables: Skills and Drives
    t_skills = Table(title="Skills & Focuses", border_style="cyan")
    t_skills.add_column("Skill", style="bold")
    t_skills.add_column("Score", justify="center", style="bold red")
    t_skills.add_column("Focuses")

    for sk, val in char.skills.items():
        f_names = [f.name for f in char.focuses if f.skill == sk]
        t_skills.add_row(sk.value, str(val), ", ".join(f_names) if f_names else "-")

    t_drives = Table(title="Drives & Statements", border_style="magenta")
    t_drives.add_column("Drive", style="bold")
    t_drives.add_column("Score", justify="center", style="bold red")
    t_drives.add_column("Statement", style="italic")

    sorted_drives = sorted(char.drives.items(), key=lambda x: x[1], reverse=True)
    for d, val in sorted_drives:
        stmt = char.drive_statements.get(d, "-")
        t_drives.add_row(d.value, str(val), f'"{stmt}"' if stmt != "-" else "-")

    console.print(t_skills)
    console.print(t_drives)

    # Talents
    t_talents = Table(title="Talents", border_style="yellow")
    t_talents.add_column("Talent", style="bold")
    t_talents.add_column("Effect")
    for t in char.talents:
        t_talents.add_row(t.display_name, t.description)
    console.print(t_talents)

    # Assets
    t_assets = Table(title="Assets", border_style="green")
    t_assets.add_column("Asset", style="bold")
    t_assets.add_column("Type")
    t_assets.add_column("Quality", justify="center")
    t_assets.add_column("Traits")
    for a in char.assets:
        t_assets.add_row(a.name, a.asset_type.value, str(a.quality), ", ".join(a.traits) if a.traits else "-")
    console.print(t_assets)


def main():
    parser = argparse.ArgumentParser(
        description="Dune: Adventures in the Imperium Character Generator & CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Random character
    p_rand = subparsers.add_parser("random", help="Generate a random player character")
    p_rand.add_argument("--faction", type=str, help="Specific faction (e.g. Fremen, Mentat, Bene Gesserit, Suk Doctor)")
    p_rand.add_argument("--archetype", type=str, help="Specific archetype (e.g. Duelist, Commander, Spy)")
    p_rand.add_argument("--house", type=str, help="Specific House (e.g. House Atreides)")
    p_rand.add_argument("--output", "-o", type=str, help="File path to save the output")
    p_rand.add_argument("--format", "-f", choices=["json", "markdown", "html", "text"], default="text")

    # NPC character
    p_npc = subparsers.add_parser("npc", help="Generate a supporting NPC character")
    p_npc.add_argument("--type", choices=["minor", "notable"], default="minor")
    p_npc.add_argument("--role", type=str, help="NPC Role (e.g. 'House Guard', 'Pilot')")
    p_npc.add_argument("--house", type=str, default="House Atreides")
    p_npc.add_argument("--output", "-o", type=str)
    p_npc.add_argument("--format", "-f", choices=["json", "markdown", "html", "text"], default="text")

    # View character file
    p_view = subparsers.add_parser("view", help="View a saved character JSON file")
    p_view.add_argument("file", type=str, help="Path to character JSON file")

    # Validate character file
    p_val = subparsers.add_parser("validate", help="Validate a character JSON file against 2d20 rules")
    p_val.add_argument("file", type=str, help="Path to character JSON file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "random":
        fac_enum = None
        if args.faction:
            for f in FactionType:
                if args.faction.lower() in f.value.lower():
                    fac_enum = f
                    break
        char = generate_random_character(
            faction=fac_enum,
            archetype_name=args.archetype,
            house=args.house,
        )

        if args.output:
            out_path = Path(args.output)
            if args.format == "html" or out_path.suffix == ".html":
                out_path.write_text(character_to_html(char), encoding="utf-8")
            elif args.format == "markdown" or out_path.suffix == ".md":
                out_path.write_text(character_to_markdown(char), encoding="utf-8")
            else:
                out_path.write_text(character_to_json(char), encoding="utf-8")
            console.print(f"[bold green]Character saved to {out_path}[/]")
        else:
            if args.format == "json":
                print(character_to_json(char))
            elif args.format == "markdown":
                print(character_to_markdown(char))
            elif args.format == "html":
                print(character_to_html(char))
            else:
                print_character_summary(char)

    elif args.command == "npc":
        if args.type == "minor":
            char = generate_minor_npc(role_name=args.role, house=args.house)
        else:
            char = generate_notable_npc(role_name=args.role, house=args.house)

        if args.output:
            save_character_to_file(char, args.output)
            console.print(f"[bold green]NPC saved to {args.output}[/]")
        else:
            print_character_summary(char)

    elif args.command == "view":
        char = load_character_from_file(args.file)
        print_character_summary(char)

    elif args.command == "validate":
        char = load_character_from_file(args.file)
        report = validate_character(char)
        
        console.print(f"[bold]Validation Report for {char.name}:[/]")
        for check, passed in report.checks.items():
            status = "[bold green]PASS[/]" if passed else "[bold red]FAIL[/]"
            console.print(f"  {status} {check}")
        
        if report.errors:
            console.print("\n[bold red]Errors:[/]")
            for err in report.errors:
                console.print(f"  - {err}")
        if report.warnings:
            console.print("\n[bold yellow]Warnings:[/]")
            for w in report.warnings:
                console.print(f"  - {w}")
                
        if report.is_valid:
            console.print("\n[bold green][OK] Character is 100% rulebook compliant![/]")
        else:
            console.print("\n[bold red][FAIL] Character has rule validation issues.[/]")


if __name__ == "__main__":
    main()
