# UNITE Playbook Visualizations

This directory contains scripts and generated visualizations for the Log4j playbook example.

## Generated Visualizations

### 1. Timeline (`log4j_timeline.png`)
- **Purpose**: Shows the chronological flow of all 16 collaboration actions across 6 phases
- **Features**: 
  - Color-coded by phase
  - Partner involvement badges on each action
  - Timeline scale (days since incident start)
- **Use**: Helps operators understand the sequence and timing of collaborative actions

### 2. Partner Involvement Matrix (`log4j_partner_matrix.png`)
- **Purpose**: Heatmap showing which defensive partners participate in each action
- **Features**:
  - 7 partner types (rows) × 16 actions (columns)
  - Color intensity indicates involvement level
  - Partner color coding on left margin
- **Use**: Quickly identify collaboration patterns and which partners are most active

### 3. Partner Capability Network (`log4j_partner_network.png`)
- **Purpose**: Network diagram showing collaboration relationships
- **Features**:
  - Partner nodes arranged in a circle
  - Edges show collaboration frequency (thickness = frequency)
  - CERT coordinator at center
  - Partner names and full descriptions
- **Use**: Visualize the collaboration ecosystem and understand partner relationships

### 4. Flowchart: Entities → Actions → Artifacts (`log4j_flowchart.png`)
- **Purpose**: Shows the flow of defensive partners performing actions that produce artifacts
- **Features**:
  - Entity boxes (defensive partners) at top
  - Action diamonds (collaboration actions) in middle
  - Artifact boxes (outputs/documents) at bottom
  - Flow arrows showing sequence and relationships
  - Log4j-specific artifacts (CVE, JNDI patterns, detection rules, patches)
- **Use**: Understand how entities, actions, and artifacts connect in the response workflow

## Regenerating Visualizations

### Prerequisites
```bash
pip install -r requirements.txt
```

### Generate All Visualizations
```bash
# Generate timeline, matrix, and network
python3 generate_visualizations.py

# Generate flowchart
python3 generate_flowchart.py
```

This will create/update all PNG files in this directory.

## Customization

The visualization script (`generate_visualizations.py`) includes:

- **Color schemes**: Professional cyber defense color palette
- **Data extraction**: Actions, partners, and phases extracted from playbook structure
- **Styling**: High-resolution (300 DPI) output, professional fonts and layouts

To customize colors, edit the `COLORS` dictionary in `generate_visualizations.py`.

## Adding Visualizations for Other Playbooks

To create visualizations for a new playbook:

1. Extract action data (sequence, name, phase, days, partners) similar to the `ACTIONS` list
2. Update `PARTNERS` list with involved partner types
3. Update `PHASES` list if phases differ
4. Run the script to generate new visualizations

## Technical Details

- **Format**: PNG (300 DPI for publication quality)
- **Libraries**: matplotlib, seaborn, numpy
- **Color scheme**: Accessible, professional palette suitable for presentations
- **Dimensions**: Optimized for markdown embedding and slides

