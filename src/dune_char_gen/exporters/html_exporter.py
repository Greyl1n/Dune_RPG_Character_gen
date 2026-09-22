"""Dune-themed printable HTML character sheet exporter."""

import html
from dune_char_gen.models.character import Character
from dune_char_gen.models.enums import SkillName, DriveName, FactionType


def character_to_html(char: Character) -> str:
    """Generate a self-contained, printable Dune-themed HTML character sheet."""
    
    # Skills rows
    skills_html = ""
    for sk in [SkillName.BATTLE, SkillName.COMMUNICATE, SkillName.DISCIPLINE, SkillName.MOVE, SkillName.UNDERSTAND]:
        score = char.get_skill(sk)
        f_list = [html.escape(f.name) for f in char.focuses if f.skill == sk]
        focuses_str = ", ".join(f_list) if f_list else '<span class="text-muted">—</span>'
        skills_html += f"""
        <tr>
            <td class="skill-name">{html.escape(sk.value)}</td>
            <td class="skill-score">{score}</td>
            <td class="skill-focuses">{focuses_str}</td>
        </tr>
        """

    # Drives rows
    drives_html = ""
    sorted_drives = sorted(char.drives.items(), key=lambda x: x[1], reverse=True)
    for d, score in sorted_drives:
        stmt = char.drive_statements.get(d, "")
        stmt_escaped = f'<em>"{html.escape(stmt)}"</em>' if stmt else '<span class="text-muted">—</span>'
        drives_html += f"""
        <tr>
            <td class="drive-name">{html.escape(d.value)}</td>
            <td class="drive-score">{score}</td>
            <td class="drive-statement">{stmt_escaped}</td>
        </tr>
        """

    # Talents cards
    talents_html = ""
    if char.talents:
        for t in char.talents:
            talents_html += f"""
            <div class="talent-card">
                <div class="talent-title">{html.escape(t.display_name)}</div>
                <div class="talent-rules">{html.escape(t.description)}</div>
            </div>
            """
    else:
        talents_html = '<p class="text-muted">No talents recorded.</p>'

    # Assets cards
    assets_html = ""
    if char.assets:
        for a in char.assets:
            traits_badges = "".join([f'<span class="badge">{html.escape(tr)}</span>' for tr in a.traits])
            quality_tag = f'<span class="badge badge-quality">Quality {a.quality}</span>' if a.quality > 0 else ""
            assets_html += f"""
            <div class="asset-card">
                <div class="asset-header">
                    <span class="asset-name">{html.escape(a.name)}</span>
                    <span class="badge badge-type">{html.escape(a.asset_type.value)}</span>
                    {quality_tag}
                </div>
                <div class="asset-traits">{traits_badges}</div>
                {f'<div class="asset-desc">{html.escape(a.description)}</div>' if a.description else ''}
            </div>
            """
    else:
        assets_html = '<p class="text-muted">No assets recorded.</p>'

    # Traits badges
    traits_html = "".join([f'<span class="trait-pill">{html.escape(tr)}</span>' for tr in char.all_traits])

    # Faction row if applicable
    faction_line = f'<div class="meta-item"><span class="meta-label">Faction:</span> <span class="meta-val">{html.escape(char.faction.value)}</span></div>' if char.faction != FactionType.NONE else ""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(char.name)} - Dune Character Sheet</title>
<style>
    :root {{
        --sand-bg: #fcf9f2;
        --card-bg: #ffffff;
        --spice-gold: #c88a38;
        --spice-dark: #8b4513;
        --spice-ember: #bc4726;
        --imperial-dark: #1b1c1e;
        --border-color: #dcd2bf;
        --text-color: #2b2825;
        --text-muted: #797167;
    }}
    
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    
    body {{
        font-family: "Palatino Linotype", "Book Antiqua", Palatino, Georgia, serif;
        background-color: var(--sand-bg);
        color: var(--text-color);
        line-height: 1.5;
        padding: 24px;
    }}
    
    .sheet-container {{
        max-width: 960px;
        margin: 0 auto;
        background: var(--card-bg);
        border: 2px solid var(--border-color);
        border-radius: 8px;
        padding: 32px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }}
    
    .header {{
        border-bottom: 2px solid var(--spice-gold);
        padding-bottom: 16px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: 16px;
    }}
    
    .char-title {{
        flex: 1;
        min-width: 280px;
    }}
    
    .char-name {{
        font-size: 32px;
        font-weight: 700;
        color: var(--imperial-dark);
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }}
    
    .char-concept {{
        font-style: italic;
        color: var(--spice-dark);
        font-size: 16px;
        margin-top: 4px;
    }}
    
    .determination-badge {{
        background: linear-gradient(135deg, var(--spice-gold), var(--spice-ember));
        color: #fff;
        padding: 8px 18px;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
    }}
    
    .determination-val {{
        font-size: 24px;
        display: block;
    }}
    
    .meta-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
        background: #f7f3ea;
        padding: 14px;
        border-radius: 6px;
        margin-bottom: 20px;
        border: 1px solid var(--border-color);
    }}
    
    .meta-item {{
        font-size: 14px;
    }}
    
    .meta-label {{
        font-weight: bold;
        color: var(--spice-dark);
    }}
    
    .traits-bar {{
        margin-bottom: 24px;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
    }}
    
    .trait-pill {{
        background: #eee6d8;
        border: 1px solid var(--spice-gold);
        color: #4a3b2c;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 13px;
        font-weight: 600;
    }}
    
    .ambition-box {{
        background: #faf4e8;
        border-left: 4px solid var(--spice-ember);
        padding: 12px 16px;
        margin-bottom: 24px;
        border-radius: 0 6px 6px 0;
    }}
    
    .ambition-title {{
        font-weight: bold;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 1px;
        color: var(--spice-ember);
        margin-bottom: 4px;
    }}
    
    .ambition-text {{
        font-size: 15px;
        font-style: italic;
    }}
    
    .main-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 28px;
    }}
    
    @media (max-width: 768px) {{
        .main-grid {{
            grid-template-columns: 1fr;
        }}
    }}
    
    .section-title {{
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 1.5px solid var(--spice-gold);
        padding-bottom: 6px;
        margin-bottom: 14px;
        color: var(--imperial-dark);
    }}
    
    table.data-table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 24px;
    }}
    
    table.data-table th {{
        text-align: left;
        padding: 8px;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: #f1ebd9;
        border-bottom: 2px solid var(--border-color);
        color: var(--spice-dark);
    }}
    
    table.data-table td {{
        padding: 8px;
        border-bottom: 1px solid var(--border-color);
        font-size: 14px;
        vertical-align: top;
    }}
    
    .skill-score, .drive-score {{
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        color: var(--spice-ember);
        width: 45px;
    }}
    
    .talent-card, .asset-card {{
        background: #faf7f0;
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 12px;
        margin-bottom: 12px;
    }}
    
    .talent-title {{
        font-weight: bold;
        color: var(--spice-dark);
        margin-bottom: 4px;
        font-size: 15px;
    }}
    
    .talent-rules {{
        font-size: 13px;
        color: #3b3733;
        line-height: 1.4;
    }}
    
    .asset-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }}
    
    .asset-name {{
        font-weight: bold;
        color: var(--imperial-dark);
        font-size: 15px;
    }}
    
    .asset-traits {{
        margin-bottom: 6px;
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
    }}
    
    .badge {{
        font-size: 11px;
        padding: 2px 6px;
        border-radius: 4px;
        background: #e2dac9;
        color: #4a4237;
    }}
    
    .badge-type {{
        background: #d8e2dc;
        color: #2b4c3f;
    }}
    
    .badge-quality {{
        background: #ffecd1;
        color: #7d4f00;
        font-weight: bold;
    }}
    
    .asset-desc {{
        font-size: 12.5px;
        font-style: italic;
        color: #555;
    }}
    
    .details-box {{
        background: #fbf9f4;
        border: 1px solid var(--border-color);
        padding: 14px;
        border-radius: 6px;
        font-size: 13.5px;
        margin-top: 14px;
    }}
    
    .details-box p {{
        margin-bottom: 8px;
    }}
    
    .text-muted {{
        color: var(--text-muted);
    }}
    
    @media print {{
        body {{
            background: #ffffff;
            padding: 0;
        }}
        .sheet-container {{
            box-shadow: none;
            border: 1px solid #999;
            padding: 16px;
        }}
    }}
</style>
</head>
<body>

<div class="sheet-container">
    <div class="header">
        <div class="char-title">
            <div class="char-name">{html.escape(char.name)}</div>
            <div class="char-concept">{html.escape(char.concept)}</div>
        </div>
        <div class="determination-badge">
            <span style="font-size: 10px; text-transform: uppercase;">Determination</span>
            <span class="determination-val">{char.determination}</span>
        </div>
    </div>

    <div class="meta-grid">
        <div class="meta-item"><span class="meta-label">House:</span> <span class="meta-val">{html.escape(char.house)}</span></div>
        <div class="meta-item"><span class="meta-label">Homeworld:</span> <span class="meta-val">{html.escape(char.homeworld)}</span></div>
        <div class="meta-item"><span class="meta-label">House Role:</span> <span class="meta-val">{html.escape(char.house_role)}</span></div>
        <div class="meta-item"><span class="meta-label">Archetype:</span> <span class="meta-val">{html.escape(char.archetype)}</span></div>
        {faction_line}
        <div class="meta-item"><span class="meta-label">Type:</span> <span class="meta-val">{html.escape(char.character_type.value)}</span></div>
    </div>

    <div class="traits-bar">
        <span style="font-weight: bold; font-size: 13px; color: var(--spice-dark);">Traits:</span>
        {traits_html}
    </div>

    {f'''
    <div class="ambition-box">
        <div class="ambition-title">Ambition (Highest Drive)</div>
        <div class="ambition-text">{html.escape(char.ambition)}</div>
    </div>
    ''' if char.ambition else ''}

    <div class="main-grid">
        <!-- Left Column: Skills & Drives -->
        <div class="left-col">
            <div class="section-title">Skills & Focuses</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Skill</th>
                        <th style="text-align: center;">Val</th>
                        <th>Focuses</th>
                    </tr>
                </thead>
                <tbody>
                    {skills_html}
                </tbody>
            </table>

            <div class="section-title">Drives & Statements</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Drive</th>
                        <th style="text-align: center;">Val</th>
                        <th>Statement</th>
                    </tr>
                </thead>
                <tbody>
                    {drives_html}
                </tbody>
            </table>
            
            <div class="section-title">Personal Details</div>
            <div class="details-box">
                {f'<p><strong>Appearance:</strong> {html.escape(char.appearance)}</p>' if char.appearance else ''}
                {f'<p><strong>Personality:</strong> {html.escape(char.personality)}</p>' if char.personality else ''}
                {f'<p><strong>Relationships:</strong> {html.escape(char.relationships)}</p>' if char.relationships else ''}
                {f'<p><strong>Notes:</strong> {html.escape(char.notes)}</p>' if char.notes else ''}
            </div>
        </div>

        <!-- Right Column: Talents & Assets -->
        <div class="right-col">
            <div class="section-title">Talents</div>
            {talents_html}

            <div class="section-title" style="margin-top: 24px;">Assets</div>
            {assets_html}
        </div>
    </div>
</div>

</body>
</html>
"""
    return html_content
