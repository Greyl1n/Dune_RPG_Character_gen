# Dune: Adventures in the Imperium — Character Generator

A complete, lore-rich, and rule-accurate Character Generator and Sheet Manager for Modiphius' ***Dune: Adventures in the Imperium*** (2d20 System).

---

## 🌟 Key Features

- **Full 2d20 Core Rulebook Implementation**:
  - **Step 1 (Concept & Faction)**: House allegiance, homeworld, role, personal traits, and faction templates (*Bene Gesserit Sister, Fremen, Mentat, Spacing Guild Agent, Suk Doctor*).
  - **Step 2 (Archetype)**: All 20 canonical archetypes (*Duelist, Commander, Courtier, Infiltrator, Scholar, Scout, Tactician, Warrior*, etc.) with primary/secondary skill designations.
  - **Step 3 & 4 (Skills & Focuses)**: 28-point allocation budget, archetype baselines, and catalog of focuses with primary-skill requirement verification.
  - **Step 5 (Talents)**: 55 canonical talents with rules text and faction prerequisites (e.g. *Prana-bindu Conditioning*, *Imperial Conditioning*, *Guildsman*, *Mind Palace*, *Voice*).
  - **Step 6 (Drives & Statements)**: Assignment of {8, 7, 6, 5, 4} and drive statements for ratings 8, 7, and 6.
  - **Step 7 (Assets)**: Tangible weapons/gear (e.g. *Crysknife, Personal Shield, Stillsuit, Poison Snooper*) and intangible assets (*Favors, Secrets, Spies, Titles*).
  - **Step 8 (Finishing Touches & Ambition)**: Ambitions aligned with the highest drive, appearance, personality, and relationships.
- **Rulebook Compliance Engine**: Real-time validation checking skill totals, bounds (4–8), primary/secondary requirements, mandatory faction talents, drive distributions, statements, and tangible asset rules.
- **Smart Random Generation**: One-click generation of thematic characters with matching lore, talents, focuses, and equipment.
- **Supporting NPC Generator**: Stat-block generator for Minor and Notable Supporting Characters (p. 145–146) for Gamemasters during sessions.
- **Multi-Format Exporters**:
  - 📄 **Themed Printable HTML**: Styled with Dune parchment & spice aesthetic, with `@media print` CSS for saving to PDF or physical printing.
  - 📝 **Markdown (`.md`)**: Formatted for Obsidian, Notion, or Discord.
  - 💾 **JSON (`.json`)**: Full state save and load roundtrip.
- **Dual Interfaces**:
  - 🖥️ **Streamlit Web Application**: Interactive wizard with live checklist and visual card previews.
  - ⚡ **Command-Line Interface (CLI)**: Fast generation, validation, and viewing directly in your terminal.

---

## 🚀 Quick Start

### 1. Launch the Standalone HTML Web Application (Zero Dependencies!)

You can run the full-featured interactive HTML app in any browser:

- **Option A (One-Click Server & Browser Launcher)**:
  ```bash
  python run_html.py
  ```
- **Option B (Directly in Browser)**:
  Simply double-click [`index.html`](file:///c:/Users/marku/Python_codes_trusted/RPG/Dune_RPG/index.html) or drag it into Chrome, Edge, or Firefox.

### 2. Launch the Streamlit Web Application

If you prefer the Streamlit interface:

```bash
python run_app.py
```
*(or `streamlit run src/app.py`)*

### 2. Use the Command-Line Interface (CLI)

#### Generate a Random Character:
```bash
# Print to terminal
python -m dune_char_gen random

# Generate a specific faction and save to HTML
python -m dune_char_gen random --faction Mentat -o mentat_sheet.html

# Generate a specific archetype and save to Markdown
python -m dune_char_gen random --archetype Duelist -o duelist.md
```

#### Generate a Supporting NPC for GM Sessions:
```bash
# Minor Supporting Character (e.g. Guard, Pilot)
python -m dune_char_gen npc --type minor --role "House Guard"

# Notable Supporting Character (Costs 3 Momentum/Threat)
python -m dune_char_gen npc --type notable --role "Infiltrator Scout"
```

#### Validate a Saved Character File:
```bash
python -m dune_char_gen validate path/to/character.json
```

#### View a Saved Character:
```bash
python -m dune_char_gen view path/to/character.json
```

---

## 📁 Project Structure

```
Dune_RPG/
├── requirements.txt                # Python dependencies
├── run_app.py                      # One-click launcher for the Streamlit web app
├── README.md                       # Project documentation
├── source_files/                   # Reference core rulebooks and character sheets
├── tests/                          # Automated unit tests
│   ├── test_rules.py               # 2d20 rules & validation tests
│   ├── test_generators.py          # Random PC and NPC generator tests
│   └── test_exporters.py           # JSON, Markdown, and HTML export tests
└── src/
    ├── app.py                      # Streamlit Web Application
    └── dune_char_gen/
        ├── __init__.py
        ├── __main__.py             # CLI entrypoint
        ├── cli.py                  # Terminal commands & rich styling
        ├── models/
        │   ├── enums.py            # Skills, Drives, Factions, Assets enums
        │   ├── character.py        # Core Character, Focus, Talent, Asset models
        │   └── validation.py       # Rulebook validation engine
        ├── data/
        │   ├── archetypes.py       # 20 canonical archetypes
        │   ├── factions.py         # Faction templates & mandatory talents
        │   ├── skills_and_focuses.py # Skills & standard focus lists
        │   ├── talents.py          # 55 canonical talents with rules text
        │   ├── drives.py           # Drives, statements, and ambition ideas
        │   ├── assets.py           # Tangible and intangible assets catalog
        │   ├── houses.py           # Houses, homeworlds, roles, domains
        │   └── names.py            # Dune-themed name generator
        ├── generators/
        │   ├── random_generator.py # Cohesive random PC generator
        │   └── npc_generator.py    # Minor & Notable Supporting Character generator
        └── exporters/
            ├── json_exporter.py    # Save/load JSON
            ├── markdown_exporter.py# Markdown character sheet
            └── html_exporter.py    # Themed printable HTML sheet
```

---

## 🧪 Running Unit Tests

Run the full automated test suite:

```bash
python -m unittest discover -s tests
```
