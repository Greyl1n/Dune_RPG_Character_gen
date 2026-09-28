"""Script to generate the standalone HTML Dune Character Generator application."""

import base64
import json
from pathlib import Path

# Load canonical data
data_path = Path("src/dune_data.json")
with open(data_path, "r", encoding="utf-8") as f:
    dune_data_json = f.read()

# Load image assets as Base64 Data URIs
icon_path = Path("assets/icon.jpg")
icon_data_uri = ""
if icon_path.exists():
    with open(icon_path, "rb") as f:
        icon_data_uri = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

bg_path = Path("assets/background.jpg")
bg_data_uri = ""
if bg_path.exists():
    with open(bg_path, "rb") as f:
        bg_data_uri = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dune: Adventures in the Imperium — Character Generator</title>
<link rel="icon" type="image/jpeg" href="__ICON_DATA_URI__">
<style>
    :root {
        --sand-bg: #f7f2e7;
        --sand-surface: #fdfbf7;
        --card-bg: #ffffff;
        --border-color: #d8cbbb;
        --border-gold: #c88a38;
        --spice-gold: #c88a38;
        --spice-ember: #bc4726;
        --spice-dark: #7a3818;
        --imperial-dark: #1b1c1e;
        --imperial-surface: #27282b;
        --text-main: #2b2825;
        --text-muted: #6e655b;
        --success: #2e7d32;
        --danger: #c62828;
        --warning: #ef6c00;
    }

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Palatino Linotype", Georgia, serif;
        background-color: var(--sand-bg);
        background-image: 
            linear-gradient(rgba(247, 242, 231, 0.88), rgba(247, 242, 231, 0.92)),
            url('__BG_DATA_URI__');
        background-attachment: fixed;
        background-position: center center;
        background-size: cover;
        background-repeat: no-repeat;
        color: var(--text-main);
        line-height: 1.5;
        padding: 0;
        margin: 0;
    }

    /* Top Imperial Header */
    .imperial-banner {
        background: linear-gradient(135deg, #18191b 0%, #2f251d 100%);
        border-bottom: 2.5px solid var(--spice-gold);
        color: #f5eedc;
        padding: 10px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.15);
    }

    .banner-title h1 {
        font-family: Georgia, "Palatino Linotype", serif;
        color: #e5b95c;
        font-size: 1.35rem;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin: 0;
    }

    .banner-title p {
        color: #c7b9a5;
        font-size: 0.8rem;
        margin-top: 2px;
        margin-bottom: 0;
        font-style: italic;
    }

    .banner-actions {
        display: flex;
        gap: 8px;
    }

    .btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 0.84rem;
        font-weight: 600;
        cursor: pointer;
        border: 1px solid transparent;
        transition: all 0.2s ease;
        text-decoration: none;
    }

    .btn-gold {
        background: linear-gradient(135deg, var(--spice-gold), #b37324);
        color: #ffffff;
        border-color: #9c6019;
    }
    .btn-gold:hover {
        background: linear-gradient(135deg, #d49542, #c88a38);
        box-shadow: 0 2px 8px rgba(200, 138, 56, 0.4);
    }

    .btn-outline {
        background: transparent;
        color: #e5b95c;
        border-color: #c88a38;
    }
    .btn-outline:hover {
        background: rgba(200, 138, 56, 0.15);
    }

    .btn-secondary {
        background: #e8ded0;
        color: #4a3f33;
        border-color: var(--border-color);
    }
    .btn-secondary:hover {
        background: #ded1c0;
    }

    /* Main Container & Layout */
    .app-container {
        max-width: 1440px;
        margin: 12px auto;
        padding: 0 16px;
        display: grid;
        grid-template-columns: minmax(0, 1fr) 280px;
        gap: 16px;
        align-items: start;
    }

    @media (max-width: 860px) {
        .app-container {
            grid-template-columns: 1fr;
        }
    }

    /* Mode Navigation Tabs */
    .nav-tabs {
        display: flex;
        gap: 6px;
        background: #eae2d3;
        padding: 5px;
        border-radius: 8px;
        margin-bottom: 12px;
        border: 1px solid var(--border-color);
        overflow-x: auto;
    }

    .nav-tab {
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.84rem;
        cursor: pointer;
        border: none;
        background: transparent;
        color: var(--text-muted);
        white-space: nowrap;
        transition: all 0.2s;
    }

    .nav-tab.active {
        background: var(--card-bg);
        color: var(--spice-dark);
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        border: 1px solid var(--border-gold);
    }

    /* Wizard Step Bar */
    .wizard-steps {
        display: flex;
        gap: 6px;
        margin-bottom: 20px;
        overflow-x: auto;
        padding-bottom: 4px;
    }

    .wizard-step-btn {
        flex: 1;
        min-width: 110px;
        text-align: center;
        padding: 8px 6px;
        background: #eee6d8;
        border: 1px solid var(--border-color);
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--text-muted);
        cursor: pointer;
        transition: all 0.2s;
    }

    .wizard-step-btn.active {
        background: var(--spice-gold);
        color: #ffffff;
        border-color: var(--spice-gold);
    }

    .wizard-step-btn.completed {
        background: #e1d8c7;
        color: var(--text-main);
        border-color: #b5a997;
    }

    /* Cards & Panels */
    .card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }

    .card-title {
        font-family: Georgia, serif;
        font-size: 1.25rem;
        color: var(--spice-dark);
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1.5px solid #ece4d4;
        padding-bottom: 8px;
    }

    /* Form Inputs */
    .form-group {
        margin-bottom: 16px;
    }

    .form-label {
        display: block;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 6px;
        color: var(--text-main);
    }

    .form-help {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 4px;
    }

    input[type="text"], input[type="number"], select, textarea {
        width: 100%;
        padding: 8px 12px;
        border: 1px solid var(--border-color);
        border-radius: 6px;
        background: #faf8f5;
        font-family: inherit;
        font-size: 0.9rem;
        color: var(--text-main);
        transition: border-color 0.2s;
    }

    input:focus, select:focus, textarea:focus {
        outline: none;
        border-color: var(--spice-gold);
        background: #ffffff;
        box-shadow: 0 0 0 2px rgba(200, 138, 56, 0.2);
    }

    .grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }

    .grid-3 {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 16px;
    }

    @media (max-width: 768px) {
        .grid-2, .grid-3 {
            grid-template-columns: 1fr;
        }
    }

    /* Skill Allocation Card */
    .skill-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 14px;
        background: #faf7f2;
        border: 1px solid #e8decb;
        border-radius: 6px;
        margin-bottom: 8px;
    }

    .skill-info {
        flex: 1;
    }

    .skill-name {
        font-weight: 700;
        font-size: 0.95rem;
    }

    .skill-tag {
        font-size: 0.7rem;
        padding: 2px 6px;
        border-radius: 4px;
        margin-left: 6px;
        font-weight: 600;
    }

    .skill-tag-primary {
        background: #ffd8a8;
        color: #7a3818;
    }

    .skill-tag-secondary {
        background: #d0ebff;
        color: #1864ab;
    }

    .counter-control {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .counter-btn {
        width: 32px;
        height: 32px;
        border-radius: 6px;
        border: 1px solid var(--border-color);
        background: #ffffff;
        font-weight: bold;
        font-size: 1.1rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .counter-btn:hover {
        background: #f0e6d6;
    }

    .counter-val {
        font-size: 1.2rem;
        font-weight: bold;
        width: 28px;
        text-align: center;
        color: var(--spice-ember);
    }

    .budget-bar {
        background: #e8decb;
        border-radius: 6px;
        height: 10px;
        overflow: hidden;
        margin-top: 8px;
        margin-bottom: 16px;
    }

    .budget-fill {
        height: 100%;
        background: var(--spice-gold);
        transition: width 0.3s;
    }

    .budget-fill.exact {
        background: var(--success);
    }

    .budget-fill.over {
        background: var(--danger);
    }

    /* Badges & Tags */
    .badge {
        display: inline-block;
        font-size: 0.75rem;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        background: #eee6d8;
        color: #4a3f33;
        border: 1px solid #d9cdbd;
    }

    .badge-quality {
        background: #fff3bf;
        color: #8f5b00;
        border-color: #ffd43b;
    }

    .badge-tangible {
        background: #d3f9d8;
        color: #2b8a3e;
        border-color: #b2f2bb;
    }

    .badge-intangible {
        background: #e7f5ff;
        color: #1971c2;
        border-color: #a5d8ff;
    }

    /* Live Audit Quick Bar (Top of Main Panel) */
    .live-audit-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 8px;
        background: #faf6ef;
        border: 1px solid #e2d4c0;
        border-left: 4px solid var(--spice-gold);
        border-radius: 6px;
        padding: 6px 12px;
        margin-bottom: 12px;
        font-size: 0.82rem;
    }

    .live-audit-metrics {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }

    .live-audit-metric {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        color: var(--spice-dark);
        font-weight: 600;
        font-size: 0.78rem;
    }

    .live-audit-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.75rem;
    }

    /* Sidebar Checklist */
    .audit-card {
        background: #ffffff;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 10px 12px;
        position: sticky;
        top: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        max-height: calc(100vh - 20px);
        overflow-y: auto;
    }

    .audit-card::-webkit-scrollbar {
        width: 5px;
    }
    .audit-card::-webkit-scrollbar-thumb {
        background: #d8cbb8;
        border-radius: 3px;
    }

    .audit-title {
        font-family: Georgia, serif;
        color: var(--spice-dark);
        font-size: 0.95rem;
        font-weight: bold;
        margin-bottom: 6px;
        border-bottom: 1.5px solid #eae2d3;
        padding-bottom: 4px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .audit-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.76rem;
        line-height: 1.25;
        padding: 2.5px 0;
        border-bottom: 1px solid #f2ece1;
    }

    .audit-item:last-child {
        border-bottom: none;
    }

    .audit-status {
        font-weight: 700;
        font-size: 0.68rem;
        padding: 1.5px 6px;
        border-radius: 10px;
        white-space: nowrap;
        margin-left: 6px;
    }

    .status-pass {
        background: #e6f4ea;
        color: #137333;
    }

    .status-fail {
        background: #fce8e6;
        color: #c5221f;
    }

    /* Printable Sheet Container */
    .sheet-view {
        background: #ffffff;
        border: 2px solid var(--border-color);
        border-radius: 8px;
        padding: 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }

    .sheet-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        border-bottom: 2px solid var(--spice-gold);
        padding-bottom: 14px;
        margin-bottom: 18px;
    }

    .sheet-name {
        font-family: Georgia, serif;
        font-size: 1.8rem;
        font-weight: bold;
        color: var(--imperial-dark);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .sheet-concept {
        font-style: italic;
        color: var(--spice-dark);
        font-size: 0.95rem;
    }

    .sheet-meta-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 8px 16px;
        background: #faf7f0;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 16px;
        border: 1px solid #eadecf;
        font-size: 0.85rem;
    }

    .table-dune {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 18px;
        font-size: 0.88rem;
    }

    .table-dune th {
        background: #f3ecd9;
        text-align: left;
        padding: 6px 10px;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 2px solid var(--border-color);
        color: var(--spice-dark);
    }

    .table-dune td {
        padding: 8px 10px;
        border-bottom: 1px solid #eee7db;
    }

    /* Print Styles */
    @media print {
        body {
            background: #ffffff;
        }
        .imperial-banner, .nav-tabs, .wizard-steps, .audit-card, .btn-no-print {
            display: none !important;
        }
        .app-container {
            grid-template-columns: 1fr;
            margin: 0;
            padding: 0;
            max-width: 100%;
        }
        .sheet-view {
            border: none;
            box-shadow: none;
            padding: 0;
        }
    }
</style>
</head>
<body>

<!-- Imperial Top Banner -->
<header class="imperial-banner">
    <div class="banner-title" style="display: flex; align-items: center; gap: 14px;">
        <img src="__ICON_DATA_URI__" alt="Dune Crest" style="width: 46px; height: 46px; border-radius: 50%; border: 2px solid var(--spice-gold); box-shadow: 0 0 10px rgba(200, 138, 56, 0.45); object-fit: cover; flex-shrink: 0;">
        <div>
            <h1>Dune: Adventures in the Imperium</h1>
            <p>2d20 System Character Generator & Sheet Architect</p>
        </div>
    </div>
    <div class="banner-actions btn-no-print">
        <button class="btn btn-gold" onclick="generateRandomPC()">🎲 Instant Random PC</button>
        <button class="btn btn-outline" onclick="printSheet()">🖨️ Print / Save PDF</button>
    </div>
</header>

<div class="app-container">
    <!-- Main Content Area -->
    <main>
        <!-- Mode Tabs -->
        <div class="nav-tabs btn-no-print">
            <button class="nav-tab active" onclick="switchMode('wizard')">🧙 Character Creator Wizard</button>
            <button class="nav-tab" onclick="switchMode('random')">🎲 Random Generator</button>
            <button class="nav-tab" onclick="switchMode('npc')">👥 Supporting NPC Generator</button>
            <button class="nav-tab" onclick="switchMode('sheet')">📄 Character Sheet Preview</button>
            <button class="nav-tab" onclick="switchMode('vault')">📂 Character Vault</button>
            <button class="nav-tab" onclick="switchMode('about')">ℹ️ About & Credits</button>
        </div>

        <!-- Live Top Rule Audit Quick-Bar (Always fully visible on page load) -->
        <div id="live-audit-banner" class="live-audit-bar btn-no-print"></div>

        <!-- ============================================== -->
        <!-- MODE 1: CHARACTER CREATOR WIZARD -->
        <!-- ============================================== -->
        <div id="mode-wizard">
            <!-- Step Navigation -->
            <div class="wizard-steps btn-no-print">
                <button class="wizard-step-btn active" onclick="goToStep(1)">1. Concept</button>
                <button class="wizard-step-btn" onclick="goToStep(2)">2. Archetype</button>
                <button class="wizard-step-btn" onclick="goToStep(3)">3. Skills & Focuses</button>
                <button class="wizard-step-btn" onclick="goToStep(4)">4. Talents</button>
                <button class="wizard-step-btn" onclick="goToStep(5)">5. Drives</button>
                <button class="wizard-step-btn" onclick="goToStep(6)">6. Assets</button>
                <button class="wizard-step-btn" onclick="goToStep(7)">7. Ambition</button>
                <button class="wizard-step-btn" onclick="goToStep(8)">8. Preview</button>
            </div>

            <!-- STEP 1: CONCEPT & FACTION -->
            <div id="step-1" class="wizard-step-panel">
                <div class="card">
                    <div class="card-title">
                        <span>Step 1: Identity & Allegiance</span>
                        <button class="btn btn-secondary" style="font-size: 0.78rem;" onclick="suggestName()">🎲 Roll Dune Name</button>
                    </div>

                    <div class="grid-2">
                        <div class="form-group">
                            <label class="form-label">Character Name</label>
                            <input type="text" id="w-name" oninput="updateChar('name', this.value)">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Faction Affiliation</label>
                            <select id="w-faction" onchange="onFactionChange(this.value)"></select>
                        </div>
                    </div>

                    <div id="w-faction-info" style="background: #faf5eb; border: 1px solid #e5d8c3; padding: 12px; border-radius: 6px; margin-bottom: 16px; font-size: 0.85rem;"></div>

                    <div class="form-group">
                        <label class="form-label">Concept Summary</label>
                        <input type="text" id="w-concept" oninput="updateChar('concept', this.value)" placeholder="E.g., Cunning spymaster serving House Atreides">
                    </div>

                    <div class="grid-3">
                        <div class="form-group">
                            <label class="form-label">House Allegiance</label>
                            <select id="w-house" onchange="updateChar('house', this.value)"></select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Homeworld</label>
                            <select id="w-homeworld" onchange="updateChar('homeworld', this.value)"></select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">House Role</label>
                            <select id="w-role" onchange="updateChar('house_role', this.value)"></select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Personal Trait</label>
                        <select id="w-trait" onchange="updateChar('personal_trait', this.value)"></select>
                    </div>

                    <div style="text-align: right; margin-top: 16px;">
                        <button class="btn btn-gold" onclick="goToStep(2)">Next: Choose Archetype →</button>
                    </div>
                </div>
            </div>

            <!-- STEP 2: ARCHETYPE -->
            <div id="step-2" class="wizard-step-panel" style="display: none;">
                <div class="card">
                    <div class="card-title">Step 2: Archetype Selection</div>
                    <div class="form-group">
                        <label class="form-label">Select Archetype</label>
                        <select id="w-archetype" onchange="onArchetypeChange(this.value)"></select>
                    </div>

                    <div id="w-arch-details" style="background: #faf7f2; border: 1px solid var(--border-color); border-radius: 6px; padding: 16px; margin-bottom: 16px;"></div>

                    <div style="display: flex; justify-content: space-between; margin-top: 16px;">
                        <button class="btn btn-secondary" onclick="goToStep(1)">← Back to Concept</button>
                        <button class="btn btn-gold" onclick="goToStep(3)">Next: Allocate Skills →</button>
                    </div>
                </div>
            </div>

            <!-- STEP 3: SKILLS & FOCUSES -->
            <div id="step-3" class="wizard-step-panel" style="display: none;">
                <div class="card">
                    <div class="card-title">
                        <span>Step 3: Skills Allocation</span>
                        <span id="skill-budget-badge" class="badge">Allocated: 28 / 28</span>
                    </div>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 8px;">
                        Base: Primary skill at 6, Secondary at 5, others at 4. Distribute 5 points freely (Min 4, Max 8, Total must equal exactly 28).
                    </p>

                    <div class="budget-bar">
                        <div id="budget-fill" class="budget-fill exact" style="width: 100%;"></div>
                    </div>

                    <div id="skills-container"></div>

                    <div class="card-title" style="margin-top: 24px;">Step 4: Focuses (Select 4)</div>
                    <p id="primary-focus-hint" style="font-size: 0.85rem; color: var(--spice-dark); margin-bottom: 12px; font-weight: 600;"></p>
                    <div id="focuses-container"></div>

                    <div style="display: flex; justify-content: space-between; margin-top: 16px;">
                        <button class="btn btn-secondary" onclick="goToStep(2)">← Back to Archetype</button>
                        <button class="btn btn-gold" onclick="goToStep(4)">Next: Choose Talents →</button>
                    </div>
                </div>
            </div>

            <!-- STEP 4: TALENTS -->
            <div id="step-4" class="wizard-step-panel" style="display: none;">
                <div class="card">
                    <div class="card-title">Step 5: Talents (Select 3)</div>
                    <div id="talent-faction-note" style="background: #faf5eb; border: 1px solid #e5d8c3; padding: 10px; border-radius: 6px; margin-bottom: 16px; font-size: 0.85rem;"></div>

                    <div id="talents-container"></div>

                    <div style="display: flex; justify-content: space-between; margin-top: 16px;">
                        <button class="btn btn-secondary" onclick="goToStep(3)">← Back to Skills</button>
                        <button class="btn btn-gold" onclick="goToStep(5)">Next: Assign Drives →</button>
                    </div>
                </div>
            </div>

            <!-- STEP 5: DRIVES & STATEMENTS -->
            <div id="step-5" class="wizard-step-panel" style="display: none;">
                <div class="card">
                    <div class="card-title">
                        <span>Step 6: Drives & Statements</span>
                        <span id="drives-status-badge" class="badge">Unique Values Check</span>
                    </div>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 14px;">
                        Rank your 5 drives by assigning the ratings <strong>8, 7, 6, 5, and 4</strong> (each value used exactly once). Provide a Drive Statement for your 3 highest drives (8, 7, 6).
                    </p>

                    <div class="grid-2">
                        <div>
                            <h4 style="font-size: 0.95rem; margin-bottom: 10px; color: var(--spice-dark);">Drive Scores</h4>
                            <div id="drives-score-container"></div>
                        </div>
                        <div>
                            <h4 style="font-size: 0.95rem; margin-bottom: 10px; color: var(--spice-dark);">Drive Statements (Ratings 8, 7, 6)</h4>
                            <div id="drive-statements-container"></div>
                        </div>
                    </div>

                    <div style="display: flex; justify-content: space-between; margin-top: 20px;">
                        <button class="btn btn-secondary" onclick="goToStep(4)">← Back to Talents</button>
                        <button class="btn btn-gold" onclick="goToStep(6)">Next: Choose Assets →</button>
                    </div>
                </div>
            </div>

            <!-- STEP 6: ASSETS -->
            <div id="step-6" class="wizard-step-panel" style="display: none;">
                <div class="card">
                    <div class="card-title">
                        <span>Step 7: Starting Assets (Choose 3)</span>
                        <span id="asset-tangible-badge" class="badge">Tangible Check</span>
                    </div>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 14px;">
                        Your character starts play with 3 assets. <strong>At least one must be Tangible</strong> (a physical weapon, tool, or protective suit).
                    </p>

                    <div id="assets-container"></div>

                    <div style="display: flex; justify-content: space-between; margin-top: 16px;">
                        <button class="btn btn-secondary" onclick="goToStep(5)">← Back to Drives</button>
                        <button class="btn btn-gold" onclick="goToStep(7)">Next: Ambition & Details →</button>
                    </div>
                </div>
            </div>

            <!-- STEP 7: AMBITION & DETAILS -->
            <div id="step-7" class="wizard-step-panel" style="display: none;">
                <div class="card">
                    <div class="card-title">Step 8: Ambition & Finishing Touches</div>
                    <div id="highest-drive-hint" style="background: #faf5eb; border: 1px solid #e5d8c3; padding: 10px; border-radius: 6px; margin-bottom: 16px; font-size: 0.85rem;"></div>

                    <div class="form-group">
                        <label class="form-label">Ambition Goal (Linked to Highest Drive)</label>
                        <select id="w-ambition-select" onchange="onAmbitionSelect(this.value)"></select>
                        <input type="text" id="w-ambition-text" style="margin-top: 6px;" oninput="updateChar('ambition', this.value)">
                    </div>

                    <div class="grid-2">
                        <div class="form-group">
                            <label class="form-label">Appearance</label>
                            <textarea id="w-appearance" rows="3" oninput="updateChar('appearance', this.value)"></textarea>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Personality</label>
                            <textarea id="w-personality" rows="3" oninput="updateChar('personality', this.value)"></textarea>
                        </div>
                    </div>

                    <div class="grid-2">
                        <div class="form-group">
                            <label class="form-label">Relationships & Allies</label>
                            <textarea id="w-relationships" rows="3" oninput="updateChar('relationships', this.value)"></textarea>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Notes & Background</label>
                            <textarea id="w-notes" rows="3" oninput="updateChar('notes', this.value)"></textarea>
                        </div>
                    </div>

                    <div style="display: flex; justify-content: space-between; margin-top: 16px;">
                        <button class="btn btn-secondary" onclick="goToStep(6)">← Back to Assets</button>
                        <button class="btn btn-gold" onclick="goToStep(8)">Review Character Sheet →</button>
                    </div>
                </div>
            </div>

            <!-- STEP 8: PREVIEW & ACTIONS -->
            <div id="step-8" class="wizard-step-panel" style="display: none;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <button class="btn btn-secondary" onclick="goToStep(7)">← Back to Ambition</button>
                    <div style="display: flex; gap: 8px;">
                        <button class="btn btn-outline" onclick="downloadJSON()">💾 Download JSON</button>
                        <button class="btn btn-outline" onclick="downloadMarkdown()">📝 Download Markdown</button>
                        <button class="btn btn-gold" onclick="printSheet()">🖨️ Print Sheet</button>
                    </div>
                </div>
                <div id="wizard-sheet-view" class="sheet-view"></div>
            </div>
        </div>

        <!-- ============================================== -->
        <!-- MODE 2: RANDOM GENERATOR -->
        <!-- ============================================== -->
        <div id="mode-random" style="display: none;">
            <div class="card">
                <div class="card-title">🎲 Instant Random Character Generator</div>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
                    Generate a fully rule-compliant player character with matching archetype, talents, focuses, drives, and gear.
                </p>

                <div class="grid-3">
                    <div class="form-group">
                        <label class="form-label">Faction Filter</label>
                        <select id="rand-faction"></select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Archetype Filter</label>
                        <select id="rand-archetype"></select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">House Allegiance</label>
                        <select id="rand-house"></select>
                    </div>
                </div>

                <button class="btn btn-gold" style="width: 100%; padding: 10px;" onclick="executeRandomGen()">✨ Roll New Character</button>
            </div>

            <div id="random-sheet-view" class="sheet-view"></div>
        </div>

        <!-- ============================================== -->
        <!-- MODE 3: SUPPORTING NPC GENERATOR -->
        <!-- ============================================== -->
        <div id="mode-npc" style="display: none;">
            <div class="card">
                <div class="card-title">👥 Supporting NPC Generator (Core Rules p. 145-146)</div>
                <div class="grid-3">
                    <div class="form-group">
                        <label class="form-label">NPC Tier</label>
                        <select id="npc-tier">
                            <option value="minor">Minor Supporting Character (1 Drive rating, 1 focus, 1 asset)</option>
                            <option value="notable">Notable Supporting Character (Costs 3 Momentum, 1 talent, 2 assets)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Role Template</label>
                        <select id="npc-role">
                            <option value="House Guard">House Guard (Battle / Blade)</option>
                            <option value="Ornithopter Pilot">Ornithopter Pilot (Move / Shield)</option>
                            <option value="House Diplomat">House Diplomat (Communicate / Contract)</option>
                            <option value="Sietch Guide">Sietch Guide (Move / Stillsuit)</option>
                            <option value="Cryptographer">Cryptographer (Understand / Filmbook)</option>
                            <option value="Field Medic">Field Medic (Understand / Snooper)</option>
                            <option value="Infiltrator Scout">Infiltrator Scout (Discipline / Bodkin)</option>
                            <option value="Quartermaster">Quartermaster (Communicate / CHOAM Permit)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">House</label>
                        <select id="npc-house"></select>
                    </div>
                </div>

                <button class="btn btn-gold" style="width: 100%; padding: 10px;" onclick="executeNPCGen()">⚔️ Generate Supporting NPC</button>
            </div>

            <div id="npc-sheet-view" class="sheet-view"></div>
        </div>

        <!-- ============================================== -->
        <!-- MODE 4: FULL SHEET PREVIEW -->
        <!-- ============================================== -->
        <div id="mode-sheet" style="display: none;">
            <div style="display: flex; justify-content: flex-end; gap: 8px; margin-bottom: 16px;" class="btn-no-print">
                <button class="btn btn-outline" onclick="downloadJSON()">💾 Download JSON</button>
                <button class="btn btn-outline" onclick="downloadMarkdown()">📝 Download Markdown</button>
                <button class="btn btn-gold" onclick="printSheet()">🖨️ Print / Save PDF</button>
            </div>
            <div id="standalone-sheet-view" class="sheet-view"></div>
        </div>

        <!-- ============================================== -->
        <!-- MODE 5: VAULT / IMPORT-EXPORT -->
        <!-- ============================================== -->
        <div id="mode-vault" style="display: none;">
            <div class="card">
                <div class="card-title">📂 Character Vault & File Management</div>

                <div class="form-group">
                    <label class="form-label">Import Character from JSON File</label>
                    <input type="file" id="vault-file-input" accept=".json" onchange="importJSON(event)">
                </div>

                <div style="display: flex; gap: 12px; margin-top: 20px;">
                    <button class="btn btn-gold" onclick="downloadJSON()">💾 Save Active Character to File (.json)</button>
                    <button class="btn btn-secondary" onclick="downloadMarkdown()">📝 Export to Markdown (.md)</button>
                    <button class="btn btn-secondary" onclick="downloadHTML()">📄 Export Standalone HTML Sheet</button>
                </div>
            </div>
        </div>

        <!-- ============================================== -->
        <!-- MODE 6: ABOUT, CREDITS & LICENSE -->
        <!-- ============================================== -->
        <div id="mode-about" style="display: none;">
            <div class="card">
                <div class="card-title">ℹ️ About Dune Character Generator</div>
                <p style="font-size: 0.95rem; margin-bottom: 14px; line-height: 1.6;">
                    The <strong>Dune: Adventures in the Imperium Character Generator & Sheet Architect</strong> is an interactive companion application designed for players and gamemasters of Modiphius Entertainment's tabletop roleplaying game <em>Dune: Adventures in the Imperium</em> (powered by the 2d20 System).
                </p>
                <div style="background: #faf7f0; border: 1px solid var(--border-color); border-radius: 6px; padding: 16px; margin-bottom: 20px;">
                    <h4 style="font-family: Georgia, serif; color: var(--spice-dark); margin-bottom: 8px;">🌟 System & Design Features</h4>
                    <ul style="padding-left: 20px; font-size: 0.88rem; line-height: 1.7; color: var(--text-main);">
                        <li><strong>Complete Planned Creation Pipeline (Steps 1–8)</strong>: Concept, Archetype, Skills, Focuses, Talents, Drives & Statements, Starting Assets, Ambition & Details.</li>
                        <li><strong>Official 2d20 Rulebook Compliance</strong>: Real-time validation audit verifying skill points total (28 points), bounds (4–8), primary/secondary baselines, mandatory faction talents, unique drive assignments ([8, 7, 6, 5, 4]), and starting assets.</li>
                        <li><strong>Comprehensive Canonical Library</strong>: 20 archetypes, 5 faction templates, 55 talents with full rules text, standard focuses across all 5 skills, and tangible/intangible assets.</li>
                        <li><strong>Smart Random PC & Supporting NPC Generators</strong>: Instant generation of fully compliant player characters and supporting characters (Minor and Notable NPCs).</li>
                        <li><strong>Multi-Format Exporters</strong>: Standalone printable HTML sheet with <code>@media print</code> formatting, Markdown, and JSON.</li>
                    </ul>
                </div>

                <div class="grid-2" style="margin-bottom: 20px;">
                    <div style="background: #faf7f0; border: 1px solid var(--border-color); border-radius: 6px; padding: 16px;">
                        <h4 style="font-family: Georgia, serif; color: var(--spice-dark); margin-bottom: 8px;">⚖️ Copyrights & Trademarks</h4>
                        <p style="font-size: 0.84rem; line-height: 1.6; color: var(--text-main); margin-bottom: 8px;">
                            <strong>Dune: Adventures in the Imperium</strong> is published by <strong>Modiphius Entertainment</strong> and developed in partnership with <strong>Legendary Entertainment</strong>.
                        </p>
                        <p style="font-size: 0.84rem; line-height: 1.6; color: var(--text-main); margin-bottom: 8px;">
                            <strong>Dune</strong> is a trademark or registered trademark of <strong>Herbert Properties LLC</strong>. All setting lore, faction names, character concepts, and related intellectual property are © Herbert Properties LLC and Legendary Entertainment.
                        </p>
                        <p style="font-size: 0.84rem; line-height: 1.6; color: var(--text-muted); font-style: italic;">
                            <strong>Unofficial Fan Companion</strong>: This software is an independent, non-commercial fan-made utility created solely for personal recreational use. It is not affiliated with, produced by, or endorsed by Modiphius Entertainment, Legendary Entertainment, or Herbert Properties LLC.
                        </p>
                    </div>

                    <div style="background: #faf7f0; border: 1px solid var(--border-color); border-radius: 6px; padding: 16px;">
                        <h4 style="font-family: Georgia, serif; color: var(--spice-dark); margin-bottom: 8px;">👥 Credits & Acknowledgments</h4>
                        <p style="font-size: 0.84rem; line-height: 1.6; color: var(--text-main); margin-bottom: 8px;">
                            <strong>Frank Herbert</strong>: For creating the masterpiece of the Dune universe.
                        </p>
                        <p style="font-size: 0.84rem; line-height: 1.6; color: var(--text-main); margin-bottom: 8px;">
                            <strong>Modiphius Entertainment Team</strong>: Nathan Dowdell, Simon Berman, Jack Norris, Jason Durall, Chris Birch, and the writers, editors, and artists who crafted the 2d20 System adaptation of Dune.
                        </p>
                    </div>
                </div>

                <div style="background: #fdfaf3; border: 1px solid var(--border-gold); border-radius: 6px; padding: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <h4 style="font-family: Georgia, serif; color: var(--spice-dark); margin: 0;">📄 License: Creative Commons Attribution-NonCommercial 4.0 International</h4>
                        <span class="badge" style="background: #eed8a1; color: #5c3b09;">CC BY-NC 4.0</span>
                    </div>
                    <p style="font-size: 0.84rem; line-height: 1.6; color: var(--text-main); margin-bottom: 8px;">
                        This fan-made project is distributed under the terms of the <strong>Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)</strong> license.
                    </p>
                    <ul style="padding-left: 20px; font-size: 0.82rem; line-height: 1.6; color: var(--text-muted); margin-bottom: 10px;">
                        <li><strong>Share</strong> — You are free to copy and redistribute the material in any medium or format.</li>
                        <li><strong>Adapt</strong> — You are free to remix, transform, and build upon the material.</li>
                        <li><strong>Attribution</strong> — You must give appropriate credit, provide a link to the license, and indicate if changes were made.</li>
                        <li><strong>NonCommercial</strong> — You may <em>not</em> use the material for commercial purposes or financial gain.</li>
                    </ul>
                    <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" rel="noopener noreferrer" style="color: var(--spice-ember); font-weight: bold; font-size: 0.84rem; text-decoration: none;">View Full Creative Commons CC BY-NC 4.0 License Terms &rarr;</a>
                </div>
            </div>
        </div>
    </main>

    <!-- Sidebar Compliance Audit Panel -->
    <aside class="btn-no-print">
        <div class="audit-card">
            <div class="audit-title">
                <span>⚖️ 2d20 Rulebook Audit</span>
                <span id="audit-badge-pill" class="audit-status status-pass">PASS</span>
            </div>
            <div id="audit-list"></div>
            <div id="audit-summary" style="margin-top: 8px; padding-top: 6px; border-top: 1px solid #f2ece1; text-align: center; font-weight: bold; font-size: 0.82rem;"></div>
        </div>
    </aside>
</div>

<!-- EMBEDDED CANONICAL DUNE DATASET -->
<script>
const DUNE_DATA = __DUNE_DATA_PLACEHOLDER__;
</script>

<!-- APP LOGIC & STATE ENGINE -->
<script>
let activeChar = null;
let currentStep = 1;

// Default character generator
function createDefaultCharacter() {
    return {
        name: "Paul Atreides",
        player_name: "",
        concept: "Noble scion and heir to House Atreides with secret Bene Gesserit conditioning.",
        character_type: "Player Character",
        house: "House Atreides",
        homeworld: "Caladan",
        house_role: "Heir",
        house_trait: "",
        faction: "Bene Gesserit Sister",
        faction_trait: "Bene Gesserit",
        archetype: "Duelist",
        archetype_trait: "Duelist",
        personal_trait: "Observant",
        skills: {
            "Battle": 8,
            "Communicate": 5,
            "Discipline": 6,
            "Move": 5,
            "Understand": 4
        },
        focuses: [
            { name: "Short Blades", skill: "Battle" },
            { name: "Dueling", skill: "Battle" },
            { name: "Body Control", skill: "Move" },
            { name: "Empathy", skill: "Communicate" }
        ],
        drives: {
            "Duty": 8,
            "Justice": 7,
            "Truth": 6,
            "Power": 5,
            "Faith": 4
        },
        drive_statements: {
            "Duty": "I serve at the pleasure of the House.",
            "Justice": "I must shield those in my care.",
            "Truth": "Respect for the truth comes close to being the basis for all morality."
        },
        ambition: "Avenge the slaughter of my kin in an honorable kanly feud.",
        determination: 1,
        talents: [
            { name: "Prana-bindu Conditioning", specialization: null, description: "Your control over your nervous and muscular systems is complete." },
            { name: "The Slow Blade", specialization: null, description: "You excel at slipping blades through personal shields." },
            { name: "Voice", specialization: null, description: "You can command others by finding the pitch that subdues their will." }
        ],
        assets: [
            { name: "Kindjal", asset_type: "Tangible", quality: 0, traits: ["Blade", "Melee", "Concealed"], description: "A traditional double-edged long dagger favored by nobility." },
            { name: "Personal Shield", asset_type: "Tangible", quality: 0, traits: ["Holtzman Field", "Kinetic Deflector"], description: "Waist-worn Holtzman generator creating a kinetic barrier." },
            { name: "Significant Favor Owed", asset_type: "Intangible", quality: 1, traits: ["Leverage", "High-Value"], description: "A blood debt or political marker owed by an influential noble." }
        ],
        appearance: "Lean aristocratic frame, keen sea-green eyes, dark tousled hair.",
        personality: "Solemn, highly perceptive, carrying the weight of ancient lineage.",
        relationships: "Heir to Duke Leto; trained by Gurney Halleck and Duncan Idaho.",
        notes: ""
    };
}

// Initialize application
window.addEventListener("DOMContentLoaded", () => {
    activeChar = createDefaultCharacter();
    populateSelectOptions();
    renderAllWizardFields();
    updateAudit();
    renderSheetViews();
});

// Populate select options
function populateSelectOptions() {
    // Factions
    const facSelect = document.getElementById("w-faction");
    const randFacSelect = document.getElementById("rand-faction");
    facSelect.innerHTML = "";
    randFacSelect.innerHTML = '<option value="">Any Faction</option>';
    for (const fKey in DUNE_DATA.factions) {
        const opt = document.createElement("option");
        opt.value = fKey;
        opt.textContent = DUNE_DATA.factions[fKey].name;
        facSelect.appendChild(opt);

        const randOpt = document.createElement("option");
        randOpt.value = fKey;
        randOpt.textContent = DUNE_DATA.factions[fKey].name;
        randFacSelect.appendChild(randOpt);
    }

    // Archetypes
    const archSelect = document.getElementById("w-archetype");
    const randArchSelect = document.getElementById("rand-archetype");
    archSelect.innerHTML = "";
    randArchSelect.innerHTML = '<option value="">Any Archetype</option>';
    for (const aName in DUNE_DATA.archetypes) {
        const opt = document.createElement("option");
        opt.value = aName;
        opt.textContent = aName;
        archSelect.appendChild(opt);

        const randOpt = document.createElement("option");
        randOpt.value = aName;
        randOpt.textContent = aName;
        randArchSelect.appendChild(randOpt);
    }

    // Houses
    const houseSelect = document.getElementById("w-house");
    const randHouseSelect = document.getElementById("rand-house");
    const npcHouseSelect = document.getElementById("npc-house");
    houseSelect.innerHTML = "";
    randHouseSelect.innerHTML = '<option value="">Any House</option>';
    npcHouseSelect.innerHTML = "";
    DUNE_DATA.houses.forEach(h => {
        const opt = document.createElement("option");
        opt.value = h;
        opt.textContent = h;
        houseSelect.appendChild(opt);

        const randOpt = document.createElement("option");
        randOpt.value = h;
        randOpt.textContent = h;
        randHouseSelect.appendChild(randOpt);

        const npcOpt = document.createElement("option");
        npcOpt.value = h;
        npcOpt.textContent = h;
        npcHouseSelect.appendChild(npcOpt);
    });

    // Homeworlds
    const hwSelect = document.getElementById("w-homeworld");
    hwSelect.innerHTML = "";
    DUNE_DATA.homeworlds.forEach(hw => {
        const opt = document.createElement("option");
        opt.value = hw;
        opt.textContent = hw;
        hwSelect.appendChild(opt);
    });

    // Roles
    const roleSelect = document.getElementById("w-role");
    roleSelect.innerHTML = "";
    DUNE_DATA.house_roles.forEach(r => {
        const opt = document.createElement("option");
        opt.value = r;
        opt.textContent = r;
        roleSelect.appendChild(opt);
    });

    // Traits
    const traitSelect = document.getElementById("w-trait");
    traitSelect.innerHTML = "";
    DUNE_DATA.personal_traits.forEach(t => {
        const opt = document.createElement("option");
        opt.value = t;
        opt.textContent = t;
        traitSelect.appendChild(opt);
    });
}

function renderAllWizardFields() {
    if (!activeChar) return;

    // Step 1
    document.getElementById("w-name").value = activeChar.name || "";
    document.getElementById("w-concept").value = activeChar.concept || "";
    document.getElementById("w-faction").value = activeChar.faction;
    document.getElementById("w-house").value = activeChar.house;
    document.getElementById("w-homeworld").value = activeChar.homeworld;
    document.getElementById("w-role").value = activeChar.house_role;
    document.getElementById("w-trait").value = activeChar.personal_trait;
    onFactionChange(activeChar.faction, false);

    // Step 2
    document.getElementById("w-archetype").value = activeChar.archetype;
    onArchetypeChange(activeChar.archetype, false);

    // Step 3
    renderSkillsAndFocuses();

    // Step 4
    renderTalents();

    // Step 5
    renderDrives();

    // Step 6
    renderAssets();

    // Step 7
    renderAmbitionAndDetails();
}

function updateChar(prop, val) {
    if (!activeChar) return;
    activeChar[prop] = val;
    updateAudit();
    renderSheetViews();
}

// Navigation between Modes
function switchMode(modeName) {
    const modes = ["wizard", "random", "npc", "sheet", "vault", "about"];
    modes.forEach(m => {
        const el = document.getElementById("mode-" + m);
        if (el) el.style.display = (m === modeName) ? "block" : "none";
    });

    document.querySelectorAll(".nav-tab").forEach((btn, idx) => {
        btn.classList.toggle("active", modes[idx] === modeName);
    });

    if (modeName === "sheet" || modeName === "wizard") {
        renderSheetViews();
    }
}

// Navigation between Wizard Steps
function goToStep(stepNum) {
    currentStep = stepNum;
    for (let i = 1; i <= 8; i++) {
        const p = document.getElementById("step-" + i);
        if (p) p.style.display = (i === stepNum) ? "block" : "none";
    }

    document.querySelectorAll(".wizard-step-btn").forEach((btn, idx) => {
        btn.classList.toggle("active", idx + 1 === stepNum);
        btn.classList.toggle("completed", idx + 1 < stepNum);
    });

    if (stepNum === 8) {
        renderSheetViews();
    }
}

// Faction Change Handler
function onFactionChange(facVal, doRender = true) {
    activeChar.faction = facVal;
    const facInfo = DUNE_DATA.factions[facVal];
    activeChar.faction_trait = facInfo ? facInfo.additional_trait : "";

    const infoBox = document.getElementById("w-faction-info");
    if (facInfo) {
        let text = `<strong>${facInfo.name}</strong> — ${facInfo.description}<br>`;
        if (facInfo.additional_trait) text += `<strong>Bonus Trait:</strong> <span class="badge">${facInfo.additional_trait}</span> `;
        if (facInfo.mandatory_talents && facInfo.mandatory_talents.length > 0) {
            const req = facInfo.require_all_mandatory ? "ALL required" : "Pick at least ONE";
            text += `| <strong>Mandatory Talents (${req}):</strong> ${facInfo.mandatory_talents.map(t => `<code>${t}</code>`).join(", ")}`;
        }
        infoBox.innerHTML = text;
    }

    if (doRender) {
        renderTalents();
        updateAudit();
        renderSheetViews();
    }
}

// Archetype Change Handler
function onArchetypeChange(archName, doRender = true) {
    activeChar.archetype = archName;
    activeChar.archetype_trait = archName;
    const arch = DUNE_DATA.archetypes[archName];

    const detailBox = document.getElementById("w-arch-details");
    if (arch) {
        detailBox.innerHTML = `
            <div style="font-size: 0.95rem; margin-bottom: 8px;">${arch.description}</div>
            <div style="display: flex; gap: 16px; flex-wrap: wrap; font-size: 0.88rem;">
                <div><strong>Primary Skill:</strong> <span class="badge" style="background:#ffd8a8; color:#7a3818;">${arch.primary_skill} (Starts at 6)</span></div>
                <div><strong>Secondary Skill:</strong> <span class="badge" style="background:#d0ebff; color:#1864ab;">${arch.secondary_skill} (Starts at 5)</span></div>
                <div><strong>Suggested Talent:</strong> <code>${arch.suggested_talent}</code></div>
            </div>
            <div style="margin-top: 8px; font-size: 0.82rem; color: var(--text-muted);">
                <strong>Philosophy:</strong> <em>${arch.drive_advice}</em>
            </div>
        `;
    }

    if (doRender) {
        renderSkillsAndFocuses();
        updateAudit();
        renderSheetViews();
    }
}

// Name Generator
function suggestName() {
    const isFremen = activeChar.faction.toLowerCase().includes("fremen");
    let name = "";
    if (isFremen) {
        const first = DUNE_DATA.names.fremen_first[Math.floor(Math.random() * DUNE_DATA.names.fremen_first.length)];
        const sietch = DUNE_DATA.names.fremen_sietch[Math.floor(Math.random() * DUNE_DATA.names.fremen_sietch.length)];
        name = Math.random() < 0.4 ? `${first} of Sietch ${sietch}` : first;
    } else {
        const first = DUNE_DATA.names.imperial_first[Math.floor(Math.random() * DUNE_DATA.names.imperial_first.length)];
        const surname = DUNE_DATA.names.imperial_surname[Math.floor(Math.random() * DUNE_DATA.names.imperial_surname.length)];
        name = `${first} ${surname}`;
    }
    activeChar.name = name;
    document.getElementById("w-name").value = name;
    updateAudit();
    renderSheetViews();
}

// Skills & Focuses Rendering
function renderSkillsAndFocuses() {
    const container = document.getElementById("skills-container");
    container.innerHTML = "";
    const arch = DUNE_DATA.archetypes[activeChar.archetype];

    let totalPoints = 0;

    DUNE_DATA.skills.forEach(sk => {
        const val = activeChar.skills[sk] || 4;
        totalPoints += val;

        const isPri = arch && arch.primary_skill === sk;
        const isSec = arch && arch.secondary_skill === sk;
        const tagHtml = isPri ? '<span class="skill-tag skill-tag-primary">Primary (6)</span>' : (isSec ? '<span class="skill-tag skill-tag-secondary">Secondary (5)</span>' : '');

        const row = document.createElement("div");
        row.className = "skill-row";
        row.innerHTML = `
            <div class="skill-info">
                <span class="skill-name">${sk}</span>
                ${tagHtml}
                <div style="font-size: 0.75rem; color: var(--text-muted);">${DUNE_DATA.skill_descriptions[sk]}</div>
            </div>
            <div class="counter-control">
                <button class="counter-btn" onclick="adjustSkill('${sk}', -1)">-</button>
                <span class="counter-val">${val}</span>
                <button class="counter-btn" onclick="adjustSkill('${sk}', 1)">+</button>
            </div>
        `;
        container.appendChild(row);
    });

    // Update budget bar
    const badge = document.getElementById("skill-budget-badge");
    const bar = document.getElementById("budget-fill");
    badge.textContent = `Allocated: ${totalPoints} / 28`;
    
    const pct = Math.min(100, (totalPoints / 28) * 100);
    bar.style.width = pct + "%";
    bar.className = "budget-fill " + (totalPoints === 28 ? "exact" : (totalPoints > 28 ? "over" : ""));

    // Render 4 Focuses
    const fcContainer = document.getElementById("focuses-container");
    fcContainer.innerHTML = "";

    const hint = document.getElementById("primary-focus-hint");
    if (arch) {
        hint.textContent = `At least 1 focus must be assigned to your primary skill: ${arch.primary_skill}.`;
    }

    while (activeChar.focuses.length < 4) {
        activeChar.focuses.push({ name: "General", skill: arch ? arch.primary_skill : "Battle" });
    }

    activeChar.focuses.forEach((fc, idx) => {
        const fRow = document.createElement("div");
        fRow.className = "grid-2";
        fRow.style.marginBottom = "10px";

        // Skill selector
        let skOptions = DUNE_DATA.skills.map(s => `<option value="${s}" ${s === fc.skill ? 'selected' : ''}>${s}</option>`).join("");
        
        // Focus name selector (standard options + custom)
        const stdList = DUNE_DATA.standard_focuses[fc.skill] || [];
        let optHtml = stdList.map(f => `<option value="${f}" ${f === fc.name ? 'selected' : ''}>${f}</option>`).join("");
        optHtml += `<option value="__custom__" ${!stdList.includes(fc.name) ? 'selected' : ''}>Custom Focus...</option>`;

        fRow.innerHTML = `
            <div>
                <label class="form-label" style="font-size:0.75rem;">Skill #${idx + 1}</label>
                <select onchange="updateFocusSkill(${idx}, this.value)">${skOptions}</select>
            </div>
            <div>
                <label class="form-label" style="font-size:0.75rem;">Focus Specialty #${idx + 1}</label>
                <select id="fc-sel-${idx}" onchange="updateFocusName(${idx}, this.value)">${optHtml}</select>
                <input type="text" id="fc-cust-${idx}" style="display: ${!stdList.includes(fc.name) ? 'block' : 'none'}; margin-top: 4px;" value="${!stdList.includes(fc.name) ? fc.name : ''}" placeholder="Enter custom focus" oninput="activeChar.focuses[${idx}].name = this.value; updateAudit();">
            </div>
        `;
        fcContainer.appendChild(fRow);
    });
}

function adjustSkill(sk, delta) {
    const curr = activeChar.skills[sk] || 4;
    const nextVal = curr + delta;
    if (nextVal >= 4 && nextVal <= 8) {
        activeChar.skills[sk] = nextVal;
        renderSkillsAndFocuses();
        updateAudit();
        renderSheetViews();
    }
}

function updateFocusSkill(idx, newSk) {
    activeChar.focuses[idx].skill = newSk;
    const std = DUNE_DATA.standard_focuses[newSk] || ["General"];
    activeChar.focuses[idx].name = std[0];
    renderSkillsAndFocuses();
    updateAudit();
    renderSheetViews();
}

function updateFocusName(idx, val) {
    const custInput = document.getElementById(`fc-cust-${idx}`);
    if (val === "__custom__") {
        custInput.style.display = "block";
        activeChar.focuses[idx].name = custInput.value || "Specialty";
    } else {
        custInput.style.display = "none";
        activeChar.focuses[idx].name = val;
    }
    updateAudit();
    renderSheetViews();
}

// Talents Rendering
function renderTalents() {
    const container = document.getElementById("talents-container");
    container.innerHTML = "";

    const facInfo = DUNE_DATA.factions[activeChar.faction];
    const facTalentNote = document.getElementById("talent-faction-note");

    if (facInfo && facInfo.mandatory_talents && facInfo.mandatory_talents.length > 0) {
        const req = facInfo.require_all_mandatory ? "ALL required" : "At least ONE required";
        facTalentNote.innerHTML = `<strong>Faction Mandatory Talents (${req}):</strong> ${facInfo.mandatory_talents.map(t => `<code>${t}</code>`).join(", ")}`;
    } else {
        facTalentNote.innerHTML = "<em>No mandatory faction talents required. Choose any 3 universal talents or archetype suggestions.</em>";
    }

    while (activeChar.talents.length < 3) {
        activeChar.talents.push({ name: "Bold", specialization: null, description: "" });
    }

    // Available talents
    const availTalents = [];
    for (const tName in DUNE_DATA.talents) {
        const t = DUNE_DATA.talents[tName];
        if (!t.faction_requirement || (activeChar.faction && activeChar.faction.toLowerCase().includes(t.faction_requirement.toLowerCase()))) {
            availTalents.push(t);
        }
    }

    activeChar.talents.forEach((tItem, idx) => {
        const tCard = document.createElement("div");
        tCard.className = "card";
        tCard.style.padding = "16px";
        tCard.style.marginBottom = "12px";

        let optHtml = availTalents.map(t => `<option value="${t.name}" ${t.name === tItem.name ? 'selected' : ''}>${t.name}${t.faction_requirement ? ` (${t.faction_requirement})` : ''}</option>`).join("");

        const tDef = DUNE_DATA.talents[tItem.name];

        tCard.innerHTML = `
            <div class="grid-2">
                <div>
                    <label class="form-label">Talent #${idx + 1}</label>
                    <select onchange="updateTalent(${idx}, this.value)">${optHtml}</select>
                </div>
                <div id="talent-spec-${idx}"></div>
            </div>
            <div style="margin-top: 10px; font-size: 0.85rem;">
                <div style="font-style: italic; color: var(--spice-dark);">${tDef ? tDef.flavor : ''}</div>
                <div style="margin-top: 4px; color: #333;">${tDef ? tDef.rules : tItem.description}</div>
            </div>
        `;
        container.appendChild(tCard);

        // Parameter selector
        const specBox = tCard.querySelector(`#talent-spec-${idx}`);
        if (tDef && tDef.skill_param) {
            specBox.innerHTML = `
                <label class="form-label">Skill Specialization</label>
                <select onchange="activeChar.talents[${idx}].specialization = this.value; renderSheetViews();">
                    ${DUNE_DATA.skills.map(s => `<option value="${s}" ${s === tItem.specialization ? 'selected' : ''}>${s}</option>`).join("")}
                </select>
            `;
            if (!tItem.specialization) tItem.specialization = DUNE_DATA.skills[0];
        } else if (tDef && tDef.drive_param) {
            specBox.innerHTML = `
                <label class="form-label">Drive Specialization</label>
                <select onchange="activeChar.talents[${idx}].specialization = this.value; renderSheetViews();">
                    ${DUNE_DATA.drives.map(d => `<option value="${d}" ${d === tItem.specialization ? 'selected' : ''}>${d}</option>`).join("")}
                </select>
            `;
            if (!tItem.specialization) tItem.specialization = "Duty";
        }
    });
}

function updateTalent(idx, newTName) {
    const tDef = DUNE_DATA.talents[newTName];
    activeChar.talents[idx] = {
        name: newTName,
        specialization: null,
        description: tDef ? tDef.rules : ""
    };
    renderTalents();
    updateAudit();
    renderSheetViews();
}

// Drives & Statements Rendering
function renderDrives() {
    const scoreContainer = document.getElementById("drives-score-container");
    scoreContainer.innerHTML = "";

    DUNE_DATA.drives.forEach(d => {
        const row = document.createElement("div");
        row.className = "skill-row";
        row.style.padding = "6px 12px";

        const val = activeChar.drives[d] || 4;
        let optHtml = [8, 7, 6, 5, 4].map(v => `<option value="${v}" ${v === val ? 'selected' : ''}>${v}</option>`).join("");

        row.innerHTML = `
            <div class="skill-info">
                <span class="skill-name">${d}</span>
                <div style="font-size: 0.72rem; color: var(--text-muted);">${DUNE_DATA.drive_descriptions[d]}</div>
            </div>
            <select style="width: 70px;" onchange="updateDriveScore('${d}', parseInt(this.value))">${optHtml}</select>
        `;
        scoreContainer.appendChild(row);
    });

    renderDriveStatements();
}

function updateDriveScore(drive, newScore) {
    activeChar.drives[drive] = newScore;
    renderDrives();
    updateAudit();
    renderSheetViews();
}

function renderDriveStatements() {
    const stmtContainer = document.getElementById("drive-statements-container");
    stmtContainer.innerHTML = "";

    // Top 3 drives (ratings >= 6)
    const topDrives = Object.keys(activeChar.drives)
        .filter(d => activeChar.drives[d] >= 6)
        .sort((a, b) => activeChar.drives[b] - activeChar.drives[a]);

    topDrives.forEach(d => {
        const sDiv = document.createElement("div");
        sDiv.style.marginBottom = "14px";
        const currStmt = activeChar.drive_statements[d] || "";

        const stdStatements = DUNE_DATA.drive_statements[d] || [];
        let optHtml = stdStatements.map(st => `<option value="${st}" ${st === currStmt ? 'selected' : ''}>${st}</option>`).join("");
        optHtml += `<option value="__custom__" ${!stdStatements.includes(currStmt) ? 'selected' : ''}>Custom Statement...</option>`;

        sDiv.innerHTML = `
            <label class="form-label" style="display:flex; justify-content:space-between;">
                <span>${d} Statement</span>
                <span class="badge" style="background:#ffd8a8; color:#7a3818;">Score: ${activeChar.drives[d]}</span>
            </label>
            <select id="stmt-sel-${d}" onchange="updateDriveStatement('${d}', this.value)">${optHtml}</select>
            <input type="text" id="stmt-cust-${d}" style="display: ${!stdStatements.includes(currStmt) ? 'block' : 'none'}; margin-top: 4px;" value="${!stdStatements.includes(currStmt) ? currStmt : ''}" placeholder="Enter custom statement" oninput="activeChar.drive_statements['${d}'] = this.value; updateAudit();">
        `;
        stmtContainer.appendChild(sDiv);
    });
}

function updateDriveStatement(drive, val) {
    const custInput = document.getElementById(`stmt-cust-${drive}`);
    if (val === "__custom__") {
        custInput.style.display = "block";
        activeChar.drive_statements[drive] = custInput.value || "I stand by my principles.";
    } else {
        custInput.style.display = "none";
        activeChar.drive_statements[drive] = val;
    }
    updateAudit();
    renderSheetViews();
}

// Assets Rendering
function renderAssets() {
    const container = document.getElementById("assets-container");
    container.innerHTML = "";

    while (activeChar.assets.length < 3) {
        activeChar.assets.push({ name: "Kindjal", asset_type: "Tangible", quality: 0, traits: [], description: "" });
    }

    const assetNames = Object.keys(DUNE_DATA.assets);

    activeChar.assets.forEach((aItem, idx) => {
        const card = document.createElement("div");
        card.className = "card";
        card.style.padding = "16px";
        card.style.marginBottom = "12px";

        let optHtml = assetNames.map(an => `<option value="${an}" ${an === aItem.name ? 'selected' : ''}>${an} (${DUNE_DATA.assets[an].asset_type})</option>`).join("");

        const aDef = DUNE_DATA.assets[aItem.name] || aItem;

        card.innerHTML = `
            <div class="grid-2">
                <div class="form-group">
                    <label class="form-label">Asset #${idx + 1}</label>
                    <select onchange="updateAsset(${idx}, this.value)">${optHtml}</select>
                </div>
                <div style="display: flex; gap: 8px; align-items: flex-end; margin-bottom: 16px;">
                    <span class="badge ${aDef.asset_type === 'Tangible' ? 'badge-tangible' : 'badge-intangible'}">${aDef.asset_type}</span>
                    ${aDef.quality > 0 ? `<span class="badge badge-quality">Quality ${aDef.quality}</span>` : ''}
                    ${(aDef.traits || []).map(tr => `<span class="badge">${tr}</span>`).join(" ")}
                </div>
            </div>
            <div style="font-size: 0.85rem; color: #555; font-style: italic;">${aDef.description || ''}</div>
        `;
        container.appendChild(card);
    });
}

function updateAsset(idx, assetName) {
    const aDef = DUNE_DATA.assets[assetName];
    if (aDef) {
        activeChar.assets[idx] = {
            name: aDef.name,
            asset_type: aDef.asset_type,
            quality: aDef.quality,
            traits: [...aDef.traits],
            description: aDef.description
        };
    }
    renderAssets();
    updateAudit();
    renderSheetViews();
}

// Ambition Rendering
function renderAmbitionAndDetails() {
    let highestDrive = "Duty";
    let highestVal = -1;
    for (const d in activeChar.drives) {
        if (activeChar.drives[d] > highestVal) {
            highestVal = activeChar.drives[d];
            highestDrive = d;
        }
    }

    const hint = document.getElementById("highest-drive-hint");
    hint.innerHTML = `Your highest-rated drive is <strong>${highestDrive} (${highestVal})</strong>. Core Rules recommend choosing an ambition aligned with this drive.`;

    const ambSelect = document.getElementById("w-ambition-select");
    const ambInput = document.getElementById("w-ambition-text");
    const stdAmbs = DUNE_DATA.ambition_examples[highestDrive] || [];

    let optHtml = stdAmbs.map(amb => `<option value="${amb}" ${amb === activeChar.ambition ? 'selected' : ''}>${amb}</option>`).join("");
    optHtml += `<option value="__custom__" ${!stdAmbs.includes(activeChar.ambition) ? 'selected' : ''}>Custom Ambition...</option>`;
    ambSelect.innerHTML = optHtml;

    ambInput.value = activeChar.ambition || (stdAmbs[0] || "");
    if (!activeChar.ambition) activeChar.ambition = stdAmbs[0] || "";

    document.getElementById("w-appearance").value = activeChar.appearance || "";
    document.getElementById("w-personality").value = activeChar.personality || "";
    document.getElementById("w-relationships").value = activeChar.relationships || "";
    document.getElementById("w-notes").value = activeChar.notes || "";
}

function onAmbitionSelect(val) {
    const ambInput = document.getElementById("w-ambition-text");
    if (val !== "__custom__") {
        ambInput.value = val;
        activeChar.ambition = val;
    }
    updateAudit();
    renderSheetViews();
}

// ==============================================
// AUDIT & VALIDATION ENGINE
// ==============================================
function updateAudit() {
    const list = document.getElementById("audit-list");
    list.innerHTML = "";

    const checks = {};
    const errors = [];

    // 1. Skill sum
    let skillSum = 0;
    for (const sk in activeChar.skills) skillSum += activeChar.skills[sk];
    checks["Skill Points Total (28)"] = (skillSum === 28);
    if (skillSum !== 28) errors.push(`Skills total is ${skillSum}/28`);

    // 2. Archetype baselines
    const arch = DUNE_DATA.archetypes[activeChar.archetype];
    if (arch) {
        checks[`Primary Skill (${arch.primary_skill} >= 6)`] = (activeChar.skills[arch.primary_skill] >= 6);
        checks[`Secondary Skill (${arch.secondary_skill} >= 5)`] = (activeChar.skills[arch.secondary_skill] >= 5);
        
        // Focus in primary
        const priFocuses = activeChar.focuses.filter(f => f.skill === arch.primary_skill);
        checks[`Focus in Primary Skill (${arch.primary_skill})`] = (priFocuses.length >= 1);
    }

    // 3. Exactly 4 Focuses
    checks["4 Focuses Chosen"] = (activeChar.focuses.length === 4);

    // 4. Talents (3 total + faction mandatory)
    checks["3 Talents Chosen"] = (activeChar.talents.length === 3);
    const facInfo = DUNE_DATA.factions[activeChar.faction];
    if (facInfo && facInfo.mandatory_talents && facInfo.mandatory_talents.length > 0) {
        const talentNames = activeChar.talents.map(t => t.name);
        if (facInfo.require_all_mandatory) {
            const allMet = facInfo.mandatory_talents.every(mt => talentNames.includes(mt));
            checks["Faction Mandatory Talents Met"] = allMet;
        } else {
            const hasOne = facInfo.mandatory_talents.some(mt => talentNames.includes(mt));
            checks["Faction Mandatory Talents Met"] = hasOne;
        }
    } else {
        checks["Faction Mandatory Talents Met"] = true;
    }

    // 5. Drives [8, 7, 6, 5, 4]
    const driveVals = Object.values(activeChar.drives).sort((a, b) => a - b);
    const drivesOk = JSON.stringify(driveVals) === JSON.stringify([4, 5, 6, 7, 8]);
    checks["Drives Assigned [8, 7, 6, 5, 4]"] = drivesOk;

    // 6. Drive Statements (ratings >= 6)
    const topDrives = Object.keys(activeChar.drives).filter(d => activeChar.drives[d] >= 6);
    let stmtsOk = (topDrives.length === 3);
    topDrives.forEach(d => {
        if (!activeChar.drive_statements[d] || !activeChar.drive_statements[d].trim()) stmtsOk = false;
    });
    checks["3 Drive Statements (for 8, 7, 6)"] = stmtsOk;

    // 7. Assets (3 assets, >= 1 tangible)
    checks["3 Starting Assets"] = (activeChar.assets.length === 3);
    const tangibleCount = activeChar.assets.filter(a => a.asset_type === "Tangible").length;
    checks["At Least 1 Tangible Asset"] = (tangibleCount >= 1);

    // Render checks
    let allPass = true;
    for (const [checkName, pass] of Object.entries(checks)) {
        if (!pass) allPass = false;
        const div = document.createElement("div");
        div.className = "audit-item";
        div.innerHTML = `
            <span>${checkName}</span>
            <span class="audit-status ${pass ? 'status-pass' : 'status-fail'}">${pass ? '✓ PASS' : '✗ FAIL'}</span>
        `;
        list.appendChild(div);
    }

    const failCount = Object.values(checks).filter(p => !p).length;

    const summary = document.getElementById("audit-summary");
    if (summary) {
        if (allPass) {
            summary.innerHTML = '<span style="color: var(--success);">✓ 100% Rulebook Compliant</span>';
        } else {
            summary.innerHTML = `<span style="color: var(--danger);">✗ ${failCount} Rule Issue${failCount > 1 ? 's' : ''} Detected</span>`;
        }
    }

    const badgePill = document.getElementById("audit-badge-pill");
    if (badgePill) {
        badgePill.className = `audit-status ${allPass ? 'status-pass' : 'status-fail'}`;
        badgePill.textContent = allPass ? 'PASS' : `${failCount} ISSUE${failCount > 1 ? 'S' : ''}`;
    }

    // Update Top Live Audit Quick Bar
    const liveBar = document.getElementById("live-audit-banner");
    if (liveBar) {
        const badgeClass = allPass ? "status-pass" : "status-fail";
        const badgeText = allPass ? "✓ 100% Rulebook Compliant" : `✗ ${failCount} Issue${failCount > 1 ? 's' : ''} (${errors.length > 0 ? errors[0] : 'Incomplete Requirements'})`;
        const skillClass = (skillSum === 28) ? "status-pass" : "status-fail";
        const focClass = (activeChar.focuses.length === 4) ? "status-pass" : "status-fail";
        const talClass = (activeChar.talents.length === 3) ? "status-pass" : "status-fail";
        const astClass = (activeChar.assets.length === 3 && tangibleCount >= 1) ? "status-pass" : "status-fail";

        liveBar.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-weight: 700; color: var(--spice-dark);">⚖️ Rules Audit:</span>
                <span class="live-audit-badge ${badgeClass}">${badgeText}</span>
            </div>
            <div class="live-audit-metrics">
                <span class="live-audit-metric">Skills: <span class="audit-status ${skillClass}" style="margin-left: 2px;">${skillSum}/28</span></span>
                <span class="live-audit-metric">Focuses: <span class="audit-status ${focClass}" style="margin-left: 2px;">${activeChar.focuses.length}/4</span></span>
                <span class="live-audit-metric">Talents: <span class="audit-status ${talClass}" style="margin-left: 2px;">${activeChar.talents.length}/3</span></span>
                <span class="live-audit-metric">Assets: <span class="audit-status ${astClass}" style="margin-left: 2px;">${activeChar.assets.length}/3</span></span>
            </div>
        `;
    }
}

// ==============================================
// SHEET PREVIEW RENDERING
// ==============================================
function renderSheetViews() {
    const html = generateSheetHTML(activeChar);
    const wizSheet = document.getElementById("wizard-sheet-view");
    const randSheet = document.getElementById("random-sheet-view");
    const stdSheet = document.getElementById("standalone-sheet-view");

    if (wizSheet) wizSheet.innerHTML = html;
    if (randSheet) randSheet.innerHTML = html;
    if (stdSheet) stdSheet.innerHTML = html;
}

function generateSheetHTML(char) {
    const traitsList = [];
    if (char.personal_trait) traitsList.push(char.personal_trait);
    if (char.archetype_trait) traitsList.push(char.archetype_trait);
    if (char.faction_trait) traitsList.push(char.faction_trait);
    if (char.house_trait) traitsList.push(char.house_trait);

    // Skills
    let skillsHtml = "";
    DUNE_DATA.skills.forEach(sk => {
        const val = char.skills[sk] || 4;
        const fList = (char.focuses || []).filter(f => f.skill === sk).map(f => f.name);
        skillsHtml += `
            <tr>
                <td style="font-weight: bold;">${sk}</td>
                <td style="text-align: center; font-weight: bold; color: var(--spice-ember); font-size: 1.1rem;">${val}</td>
                <td>${fList.length > 0 ? fList.join(", ") : '<span style="color:#aaa;">—</span>'}</td>
            </tr>
        `;
    });

    // Drives
    let drivesHtml = "";
    const sortedDrives = Object.keys(char.drives).sort((a, b) => char.drives[b] - char.drives[a]);
    sortedDrives.forEach(d => {
        const val = char.drives[d];
        const stmt = char.drive_statements[d] || "";
        drivesHtml += `
            <tr>
                <td style="font-weight: bold;">${d}</td>
                <td style="text-align: center; font-weight: bold; color: var(--spice-ember); font-size: 1.1rem;">${val}</td>
                <td style="font-style: italic;">${stmt ? `"${stmt}"` : '<span style="color:#aaa;">—</span>'}</td>
            </tr>
        `;
    });

    // Talents
    let talentsHtml = "";
    (char.talents || []).forEach(t => {
        const specStr = t.specialization ? ` (${t.specialization})` : "";
        talentsHtml += `
            <div style="background: #faf7f2; border: 1px solid var(--border-color); border-radius: 6px; padding: 10px 14px; margin-bottom: 8px;">
                <div style="font-weight: bold; color: var(--spice-dark); font-size: 0.95rem;">${t.name}${specStr}</div>
                <div style="font-size: 0.84rem; margin-top: 4px; color: #333;">${t.description}</div>
            </div>
        `;
    });

    // Assets
    let assetsHtml = "";
    (char.assets || []).forEach(a => {
        const traitsBadges = (a.traits || []).map(tr => `<span class="badge">${tr}</span>`).join(" ");
        assetsHtml += `
            <div style="background: #faf7f2; border: 1px solid var(--border-color); border-radius: 6px; padding: 10px 14px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-weight: bold; font-size: 0.95rem;">${a.name}</span>
                    <span class="badge ${a.asset_type === 'Tangible' ? 'badge-tangible' : 'badge-intangible'}">${a.asset_type}</span>
                    ${a.quality > 0 ? `<span class="badge badge-quality">Quality ${a.quality}</span>` : ''}
                </div>
                <div style="margin-bottom: 4px;">${traitsBadges}</div>
                <div style="font-size: 0.8rem; font-style: italic; color: #555;">${a.description || ''}</div>
            </div>
        `;
    });

    return `
        <div class="sheet-header">
            <div>
                <div class="sheet-name">${char.name}</div>
                <div class="sheet-concept">${char.concept || ''}</div>
            </div>
            <div style="background: linear-gradient(135deg, var(--spice-gold), var(--spice-ember)); color:#fff; padding: 6px 16px; border-radius: 6px; text-align: center;">
                <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.5px;">Determination</div>
                <div style="font-size: 1.4rem; font-weight: bold;">${char.determination || 1}</div>
            </div>
        </div>

        <div class="sheet-meta-grid">
            <div><strong>House:</strong> ${char.house} (${char.homeworld})</div>
            <div><strong>Role:</strong> ${char.house_role}</div>
            <div><strong>Archetype:</strong> ${char.archetype}</div>
            ${char.faction && char.faction !== 'None (House Retainer / Independent)' ? `<div><strong>Faction:</strong> ${char.faction}</div>` : ''}
            <div><strong>Traits:</strong> ${traitsList.map(t => `<span class="badge">${t}</span>`).join(" ")}</div>
        </div>

        ${char.ambition ? `
        <div style="background: #faf5eb; border-left: 4px solid var(--spice-ember); padding: 10px 14px; border-radius: 0 6px 6px 0; margin-bottom: 18px;">
            <div style="font-size: 0.72rem; text-transform: uppercase; font-weight: bold; color: var(--spice-ember); letter-spacing: 0.5px;">Ambition</div>
            <div style="font-style: italic; font-size: 0.95rem;">${char.ambition}</div>
        </div>
        ` : ''}

        <div class="grid-2">
            <div>
                <h4 style="font-family: Georgia, serif; font-size: 1.1rem; color: var(--imperial-dark); border-bottom: 1.5px solid var(--spice-gold); padding-bottom: 4px; margin-bottom: 10px;">Skills & Focuses</h4>
                <table class="table-dune">
                    <thead><tr><th>Skill</th><th style="text-align:center;">Val</th><th>Focuses</th></tr></thead>
                    <tbody>${skillsHtml}</tbody>
                </table>

                <h4 style="font-family: Georgia, serif; font-size: 1.1rem; color: var(--imperial-dark); border-bottom: 1.5px solid var(--spice-gold); padding-bottom: 4px; margin-bottom: 10px;">Drives & Statements</h4>
                <table class="table-dune">
                    <thead><tr><th>Drive</th><th style="text-align:center;">Val</th><th>Statement</th></tr></thead>
                    <tbody>${drivesHtml}</tbody>
                </table>
            </div>

            <div>
                <h4 style="font-family: Georgia, serif; font-size: 1.1rem; color: var(--imperial-dark); border-bottom: 1.5px solid var(--spice-gold); padding-bottom: 4px; margin-bottom: 10px;">Talents</h4>
                ${talentsHtml}

                <h4 style="font-family: Georgia, serif; font-size: 1.1rem; color: var(--imperial-dark); border-bottom: 1.5px solid var(--spice-gold); padding-bottom: 4px; margin-bottom: 10px; margin-top: 18px;">Starting Assets</h4>
                ${assetsHtml}
            </div>
        </div>

        ${(char.appearance || char.personality || char.relationships || char.notes) ? `
        <div style="margin-top: 18px; padding: 14px; background: #faf7f2; border: 1px solid var(--border-color); border-radius: 6px; font-size: 0.85rem;">
            ${char.appearance ? `<p style="margin-bottom: 6px;"><strong>Appearance:</strong> ${char.appearance}</p>` : ''}
            ${char.personality ? `<p style="margin-bottom: 6px;"><strong>Personality:</strong> ${char.personality}</p>` : ''}
            ${char.relationships ? `<p style="margin-bottom: 6px;"><strong>Relationships:</strong> ${char.relationships}</p>` : ''}
            ${char.notes ? `<p><strong>Notes:</strong> ${char.notes}</p>` : ''}
        </div>
        ` : ''}
    `;
}

// ==============================================
// RANDOM PC GENERATOR ALGORITHM
// ==============================================
function generateRandomPC(factionOverride = null, archetypeOverride = null, houseOverride = null) {
    // 1. Faction
    let faction = factionOverride;
    if (!faction) {
        const facKeys = Object.keys(DUNE_DATA.factions);
        // Bias slightly to none
        const pool = ["None (House Retainer / Independent)", "None (House Retainer / Independent)", ...facKeys];
        faction = pool[Math.floor(Math.random() * pool.length)];
    }
    const facInfo = DUNE_DATA.factions[faction];

    // 2. Archetype
    let archetype = archetypeOverride;
    if (!archetype) {
        if (facInfo && facInfo.suggested_archetypes && facInfo.suggested_archetypes.length > 0 && Math.random() < 0.8) {
            archetype = facInfo.suggested_archetypes[Math.floor(Math.random() * facInfo.suggested_archetypes.length)];
        } else {
            const allArchs = Object.keys(DUNE_DATA.archetypes);
            archetype = allArchs[Math.floor(Math.random() * allArchs.length)];
        }
    }
    const arch = DUNE_DATA.archetypes[archetype];

    // 3. House & Homeworld
    let house = houseOverride;
    if (!house) {
        house = faction === "Fremen" ? "Independent / Fremen Tribe" : DUNE_DATA.houses[Math.floor(Math.random() * DUNE_DATA.houses.length)];
    }

    let homeworld = "Caladan";
    if (faction === "Fremen") homeworld = "Arrakis (Dune)";
    else if (house.includes("Atreides")) homeworld = "Caladan";
    else if (house.includes("Harkonnen")) homeworld = "Giedi Prime";
    else if (house.includes("Corrino")) homeworld = "Kaitain";
    else homeworld = DUNE_DATA.homeworlds[Math.floor(Math.random() * DUNE_DATA.homeworlds.length)];

    // 4. Name & Role
    let name = "";
    if (faction === "Fremen") {
        const first = DUNE_DATA.names.fremen_first[Math.floor(Math.random() * DUNE_DATA.names.fremen_first.length)];
        const sietch = DUNE_DATA.names.fremen_sietch[Math.floor(Math.random() * DUNE_DATA.names.fremen_sietch.length)];
        name = Math.random() < 0.4 ? `${first} of Sietch ${sietch}` : first;
    } else {
        const first = DUNE_DATA.names.imperial_first[Math.floor(Math.random() * DUNE_DATA.names.imperial_first.length)];
        const surname = DUNE_DATA.names.imperial_surname[Math.floor(Math.random() * DUNE_DATA.names.imperial_surname.length)];
        name = `${first} ${surname}`;
    }

    const role = DUNE_DATA.house_roles[Math.floor(Math.random() * DUNE_DATA.house_roles.length)];
    const trait = DUNE_DATA.personal_traits[Math.floor(Math.random() * DUNE_DATA.personal_traits.length)];

    // 5. Skills (Primary=6, Secondary=5, others=4, +5 free points, max 8)
    const skills = {};
    DUNE_DATA.skills.forEach(s => skills[s] = 4);
    skills[arch.primary_skill] = 6;
    skills[arch.secondary_skill] = 5;

    let pointsLeft = 5;
    const candidates = [arch.primary_skill, arch.primary_skill, arch.secondary_skill, ...DUNE_DATA.skills];
    while (pointsLeft > 0) {
        const sk = candidates[Math.floor(Math.random() * candidates.length)];
        if (skills[sk] < 8) {
            skills[sk]++;
            pointsLeft--;
        }
    }

    // 6. Focuses (4 total, >= 1 in primary)
    const focuses = [];
    const priSug = (arch.suggested_focuses || []).filter(f => (DUNE_DATA.standard_focuses[arch.primary_skill] || []).includes(f));
    if (priSug.length > 0) {
        focuses.push({ name: priSug[0], skill: arch.primary_skill });
    } else {
        const stdPri = DUNE_DATA.standard_focuses[arch.primary_skill];
        focuses.push({ name: stdPri[Math.floor(Math.random() * stdPri.length)], skill: arch.primary_skill });
    }

    // Add second suggested focus
    const remSug = (arch.suggested_focuses || []).filter(f => !focuses.some(fc => fc.name === f));
    if (remSug.length > 0) {
        let fName = remSug[0];
        let assignedSk = arch.secondary_skill;
        for (const sk in DUNE_DATA.standard_focuses) {
            if (DUNE_DATA.standard_focuses[sk].includes(fName)) {
                assignedSk = sk;
                break;
            }
        }
        focuses.push({ name: fName, skill: assignedSk });
    }

    while (focuses.length < 4) {
        const sk = DUNE_DATA.skills[Math.floor(Math.random() * DUNE_DATA.skills.length)];
        const stdList = (DUNE_DATA.standard_focuses[sk] || []).filter(f => !focuses.some(fc => fc.name === f));
        if (stdList.length > 0) {
            focuses.push({ name: stdList[Math.floor(Math.random() * stdList.length)], skill: sk });
        }
    }

    // 7. Talents
    const talents = [];
    const takenNames = new Set();

    // Mandatory faction talents
    if (facInfo && facInfo.mandatory_talents && facInfo.mandatory_talents.length > 0) {
        if (facInfo.require_all_mandatory) {
            facInfo.mandatory_talents.forEach(mt => {
                const tDef = DUNE_DATA.talents[mt];
                talents.push({ name: mt, specialization: null, description: tDef ? tDef.rules : "" });
                takenNames.add(mt);
            });
        } else {
            const mt = facInfo.mandatory_talents[Math.floor(Math.random() * facInfo.mandatory_talents.length)];
            const tDef = DUNE_DATA.talents[mt];
            talents.push({ name: mt, specialization: null, description: tDef ? tDef.rules : "" });
            takenNames.add(mt);
        }
    }

    // Suggested archetype talent
    if (arch.suggested_talent && !takenNames.has(arch.suggested_talent)) {
        const tDef = DUNE_DATA.talents[arch.suggested_talent];
        if (tDef && (!tDef.faction_requirement || faction.toLowerCase().includes(tDef.faction_requirement.toLowerCase()))) {
            talents.push({ name: arch.suggested_talent, specialization: null, description: tDef.rules });
            takenNames.add(arch.suggested_talent);
        }
    }

    // Fill remaining
    const avail = Object.keys(DUNE_DATA.talents).filter(tn => {
        const t = DUNE_DATA.talents[tn];
        return !takenNames.has(tn) && (!t.faction_requirement || faction.toLowerCase().includes(t.faction_requirement.toLowerCase()));
    });

    while (talents.length < 3 && avail.length > 0) {
        const pickIdx = Math.floor(Math.random() * avail.length);
        const tn = avail.splice(pickIdx, 1)[0];
        const tDef = DUNE_DATA.talents[tn];
        talents.push({ name: tn, specialization: tDef.skill_param ? arch.primary_skill : null, description: tDef.rules });
        takenNames.add(tn);
    }

    // 8. Drives [8, 7, 6, 5, 4]
    const driveOrder = [...DUNE_DATA.drives].sort(() => Math.random() - 0.5);
    const driveScores = [8, 7, 6, 5, 4];
    const drives = {};
    driveOrder.forEach((d, idx) => drives[d] = driveScores[idx]);

    // Statements for top 3
    const drive_statements = {};
    const topDrives = Object.keys(drives).filter(d => drives[d] >= 6);
    topDrives.forEach(d => {
        const stmts = DUNE_DATA.drive_statements[d] || ["I will uphold my honor."];
        drive_statements[d] = stmts[Math.floor(Math.random() * stmts.length)];
    });

    // Ambition (tied to highest drive)
    const highestDrive = Object.keys(drives).reduce((a, b) => drives[a] > drives[b] ? a : b);
    const ambPool = DUNE_DATA.ambition_examples[highestDrive] || ["Advance the prestige of my House."];
    const ambition = ambPool[Math.floor(Math.random() * ambPool.length)];

    // 9. Assets (3 total, >= 1 tangible)
    const assets = [];
    let tangiblePicks = ["Kindjal", "Personal Shield", "Stillsuit", "Crysknife", "Blade", "Maula Pistol"];
    if (faction === "Fremen") tangiblePicks = ["Crysknife", "Stillsuit", "Fremkit"];
    else if (archetype === "Duelist") tangiblePicks = ["Kindjal", "Personal Shield", "Blade"];

    const firstTan = tangiblePicks[Math.floor(Math.random() * tangiblePicks.length)];
    const def1 = DUNE_DATA.assets[firstTan];
    assets.push({ name: def1.name, asset_type: def1.asset_type, quality: def1.quality, traits: [...def1.traits], description: def1.description });

    // Intangible pick
    const intangibles = Object.keys(DUNE_DATA.assets).filter(k => DUNE_DATA.assets[k].asset_type === "Intangible");
    const secName = intangibles[Math.floor(Math.random() * intangibles.length)];
    const def2 = DUNE_DATA.assets[secName];
    assets.push({ name: def2.name, asset_type: def2.asset_type, quality: def2.quality, traits: [...def2.traits], description: def2.description });

    // 3rd asset
    const allRem = Object.keys(DUNE_DATA.assets).filter(k => k !== firstTan && k !== secName);
    const thirdName = allRem[Math.floor(Math.random() * allRem.length)];
    const def3 = DUNE_DATA.assets[thirdName];
    assets.push({ name: def3.name, asset_type: def3.asset_type, quality: def3.quality, traits: [...def3.traits], description: def3.description });

    activeChar = {
        name,
        player_name: "",
        concept: `${trait} ${archetype} serving ${house} as ${role}.`,
        character_type: "Player Character",
        house,
        homeworld,
        house_role: role,
        house_trait: "",
        faction,
        faction_trait: facInfo.additional_trait,
        archetype,
        archetype_trait: archetype,
        personal_trait: trait,
        skills,
        focuses,
        drives,
        drive_statements,
        ambition,
        determination: 1,
        talents,
        assets,
        appearance: "Tailored garments bearing the crest of the House, accompanied by keen weapons.",
        personality: `${trait}, sharp-minded, and steadfast in purpose.`,
        relationships: `Answers to the high council of ${house}.`,
        notes: "Generated Dune 2d20 Character."
    };

    renderAllWizardFields();
    updateAudit();
    renderSheetViews();
}

function executeRandomGen() {
    const f = document.getElementById("rand-faction").value || null;
    const a = document.getElementById("rand-archetype").value || null;
    const h = document.getElementById("rand-house").value || null;
    generateRandomPC(f, a, h);
}

// ==============================================
// SUPPORTING NPC GENERATOR
// ==============================================
function executeNPCGen() {
    const tier = document.getElementById("npc-tier").value;
    const role = document.getElementById("npc-role").value;
    const house = document.getElementById("npc-house").value;

    const first = DUNE_DATA.names.imperial_first[Math.floor(Math.random() * DUNE_DATA.names.imperial_first.length)];
    const surname = DUNE_DATA.names.imperial_surname[Math.floor(Math.random() * DUNE_DATA.names.imperial_surname.length)];
    const name = `${first} ${surname}`;

    let primarySk = "Battle";
    let assetName = "Blade";
    if (role.includes("Pilot")) { primarySk = "Move"; assetName = "Personal Shield"; }
    else if (role.includes("Diplomat") || role.includes("Quartermaster")) { primarySk = "Communicate"; assetName = "House Retainer Contract"; }
    else if (role.includes("Guide")) { primarySk = "Move"; assetName = "Stillsuit"; }
    else if (role.includes("Cryptographer") || role.includes("Medic")) { primarySk = "Understand"; assetName = "Filmbook & Reader"; }
    else if (role.includes("Infiltrator")) { primarySk = "Discipline"; assetName = "Bodkin"; }

    const remSkills = DUNE_DATA.skills.filter(s => s !== primarySk).sort(() => Math.random() - 0.5);

    if (tier === "minor") {
        // Minor NPC: 1 skill at 6, 2 at 5, 2 at 4. 1 focus. 1 asset. Single drive 5.
        const skills = { [primarySk]: 6, [remSkills[0]]: 5, [remSkills[1]]: 5, [remSkills[2]]: 4, [remSkills[3]]: 4 };
        const stdF = DUNE_DATA.standard_focuses[primarySk] || ["General"];
        const aDef = DUNE_DATA.assets[assetName];

        const npcChar = {
            name: `${name} (${role})`,
            player_name: "Gamemaster",
            concept: `Minor Supporting Character: ${role} of ${house}`,
            character_type: "Minor Supporting Character",
            house,
            homeworld: "Unknown",
            house_role: role,
            faction: "None (House Retainer / Independent)",
            archetype: role,
            personal_trait: role,
            skills,
            focuses: [{ name: stdF[0], skill: primarySk }],
            drives: { "Duty": 5, "Faith": 5, "Justice": 5, "Power": 5, "Truth": 5 },
            drive_statements: { "Duty": "Single Drive rating (5) for all tests." },
            ambition: `Faithfully execute orders as ${role}.`,
            determination: 1,
            talents: [],
            assets: [{ name: aDef.name, asset_type: aDef.asset_type, quality: aDef.quality, traits: [...aDef.traits], description: aDef.description }],
            appearance: "", personality: "", relationships: "", notes: "Minor Supporting NPC"
        };
        document.getElementById("npc-sheet-view").innerHTML = generateSheetHTML(npcChar);
    } else {
        // Notable NPC: 1 at 7, 1 at 6, 1 at 5, 2 at 4. 2 focuses. 1 talent. 2 assets.
        const skills = { [primarySk]: 7, [remSkills[0]]: 6, [remSkills[1]]: 5, [remSkills[2]]: 4, [remSkills[3]]: 4 };
        const std1 = DUNE_DATA.standard_focuses[primarySk] || ["Tactics"];
        const std2 = DUNE_DATA.standard_focuses[remSkills[0]] || ["Composure"];
        const aDef1 = DUNE_DATA.assets[assetName];
        const aDef2 = DUNE_DATA.assets["Personal Shield"];

        const tDef = DUNE_DATA.talents["Bold"];

        const npcChar = {
            name: `${name} (Notable ${role})`,
            player_name: "Gamemaster",
            concept: `Notable Supporting Character: Veteran ${role} of ${house}`,
            character_type: "Notable Supporting Character",
            house,
            homeworld: "Unknown",
            house_role: role,
            faction: "None (House Retainer / Independent)",
            archetype: role,
            personal_trait: "Veteran",
            skills,
            focuses: [{ name: std1[0], skill: primarySk }, { name: std2[0], skill: remSkills[0] }],
            drives: { "Duty": 8, "Faith": 7, "Justice": 6, "Power": 5, "Truth": 5 },
            drive_statements: { "Duty": "I stand resolute in service." },
            ambition: `Advance the prestige of ${house}.`,
            determination: 1,
            talents: [{ name: "Bold", specialization: primarySk, description: tDef.rules }],
            assets: [
                { name: aDef1.name, asset_type: aDef1.asset_type, quality: aDef1.quality, traits: [...aDef1.traits], description: aDef1.description },
                { name: aDef2.name, asset_type: aDef2.asset_type, quality: aDef2.quality, traits: [...aDef2.traits], description: aDef2.description }
            ],
            appearance: "", personality: "", relationships: "", notes: "Notable Supporting NPC (Cost: 3 Momentum/Threat)"
        };
        document.getElementById("npc-sheet-view").innerHTML = generateSheetHTML(npcChar);
    }
}

// ==============================================
// EXPORT & PRINT UTILITIES
// ==============================================
function printSheet() {
    window.print();
}

function downloadJSON() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(activeChar, null, 2));
    const a = document.createElement("a");
    a.href = dataStr;
    a.download = `${activeChar.name.replace(/\\s+/g, "_")}.json`;
    a.click();
}

function downloadMarkdown() {
    let md = `# ${activeChar.name}\\n*${activeChar.concept}*\\n\\n`;
    md += `## Identity & House\\n- **House:** ${activeChar.house} (${activeChar.homeworld})\\n- **Role:** ${activeChar.house_role}\\n- **Archetype:** ${activeChar.archetype}\\n- **Faction:** ${activeChar.faction}\\n\\n`;
    md += `## Ambition\\n> ${activeChar.ambition}\\n\\n`;
    md += `## Skills & Focuses\\n| Skill | Score | Focuses |\\n| :--- | :---: | :--- |\\n`;
    DUNE_DATA.skills.forEach(s => {
        const val = activeChar.skills[s] || 4;
        const fl = (activeChar.focuses || []).filter(f => f.skill === s).map(f => f.name).join(", ");
        md += `| **${s}** | **${val}** | ${fl || "—"} |\\n`;
    });
    md += `\\n## Drives\\n| Drive | Score | Statement |\\n| :--- | :---: | :--- |\\n`;
    for (const d in activeChar.drives) {
        md += `| **${d}** | **${activeChar.drives[d]}** | *"${activeChar.drive_statements[d] || '—'}"* |\\n`;
    }
    md += `\\n## Talents\\n`;
    (activeChar.talents || []).forEach(t => {
        md += `### ${t.name}${t.specialization ? ` (${t.specialization})` : ''}\\n${t.description}\\n\\n`;
    });
    md += `## Assets\\n`;
    (activeChar.assets || []).forEach(a => {
        md += `- **${a.name}** (${a.asset_type}) [Quality ${a.quality}]: *${a.description}*\\n`;
    });

    const dataStr = "data:text/markdown;charset=utf-8," + encodeURIComponent(md);
    const a = document.createElement("a");
    a.href = dataStr;
    a.download = `${activeChar.name.replace(/\\s+/g, "_")}.md`;
    a.click();
}

function downloadHTML() {
    const fullHtml = `<!DOCTYPE html><html><head><meta charset="UTF-8"><title>${activeChar.name} - Dune Character Sheet</title><style>${document.querySelector("style").innerHTML}</style></head><body><div class="sheet-view">${generateSheetHTML(activeChar)}</div></body></html>`;
    const dataStr = "data:text/html;charset=utf-8," + encodeURIComponent(fullHtml);
    const a = document.createElement("a");
    a.href = dataStr;
    a.download = `${activeChar.name.replace(/\\s+/g, "_")}_sheet.html`;
    a.click();
}

function importJSON(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            activeChar = JSON.parse(e.target.result);
            renderAllWizardFields();
            updateAudit();
            renderSheetViews();
            alert("Character loaded successfully into active session!");
            switchMode("wizard");
        } catch (err) {
            alert("Error parsing JSON file: " + err);
        }
    };
    reader.readAsText(file);
}
</script>

</body>
</html>
"""

# Replace placeholders with actual data
final_html = (
    html_template
    .replace("__DUNE_DATA_PLACEHOLDER__", dune_data_json)
    .replace("__ICON_DATA_URI__", icon_data_uri)
    .replace("__BG_DATA_URI__", bg_data_uri)
)

# Write to root index.html
Path("index.html").write_text(final_html, encoding="utf-8")
print("Generated index.html successfully! Size:", len(final_html))

# Also write to artifact directory for generative_ui
artifact_path = Path(r"C:\Users\marku\.gemini\antigravity\brain\455876f1-abd5-4803-a0fc-ead687aa4b3c\dune_character_generator.html")
artifact_path.write_text(final_html, encoding="utf-8")
print(f"Generated artifact at {artifact_path} successfully!")
