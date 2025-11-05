#!/usr/bin/env python3
"""
Generate colorful visualizations for the Log4j playbook.
Creates three visualizations:
1. Timeline showing actions and phases
2. Partner involvement matrix (heatmap)
3. Partner capability map (network diagram)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches
from datetime import datetime, timedelta

# Set style for professional-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 9

# Color scheme - professional cyber defense colors
COLORS = {
    'phases': {
        'Phase 1: Discovery & Assessment': '#1f77b4',  # Blue
        'Phase 2: Coordination': '#ff7f0e',             # Orange
        'Phase 3: Detection & Intelligence': '#2ca02c', # Green
        'Phase 4: Information Sharing': '#d62728',     # Red
        'Phase 5: Mitigation & Hardening': '#9467bd',   # Purple
        'Phase 6: Learning & Improvement': '#8c564b'    # Brown
    },
    'partners': {
        'CERT': '#2E86AB',  # Blue - Government
        'CSP': '#A23B72',   # Purple - Service providers
        'CLO': '#F18F01',   # Orange - Cloud
        'IT': '#C73E1D',    # Red - Vendors
        'ENT': '#6A994E',   # Green - Enterprise
        'THR': '#BC4749',   # Dark red - Intelligence
        'ISP': '#219EBC'    # Cyan - Infrastructure
    },
    'background': '#f8f9fa',
    'text': '#212529'
}

# Playbook data extracted from the markdown
ACTIONS = [
    {'seq': 1, 'name': 'Assess', 'phase': 'Phase 1: Discovery & Assessment', 'days': [0, 1], 'partners': ['CERT', 'IT', 'THR']},
    {'seq': 2, 'name': 'Prioritize', 'phase': 'Phase 1: Discovery & Assessment', 'days': [1, 1], 'partners': ['CERT']},
    {'seq': 3, 'name': 'Partner', 'phase': 'Phase 2: Coordination', 'days': [1, 2], 'partners': ['CERT', 'CLO', 'CSP', 'IT', 'THR']},
    {'seq': 4, 'name': 'Form', 'phase': 'Phase 2: Coordination', 'days': [1, 2], 'partners': ['CERT']},
    {'seq': 5, 'name': 'Hunt', 'phase': 'Phase 3: Detection & Intelligence', 'days': [1, 7], 'partners': ['ENT', 'CSP', 'CLO', 'THR']},
    {'seq': 6, 'name': 'Report', 'phase': 'Phase 3: Detection & Intelligence', 'days': [1, 30], 'partners': ['CERT', 'ENT', 'CSP', 'CLO', 'THR', 'IT', 'ISP']},
    {'seq': 7, 'name': 'Analyze', 'phase': 'Phase 3: Detection & Intelligence', 'days': [1, 30], 'partners': ['CERT', 'THR', 'IT']},
    {'seq': 8, 'name': 'Share', 'phase': 'Phase 4: Information Sharing', 'days': [1, 14], 'partners': ['CERT', 'CSP', 'THR', 'IT']},
    {'seq': 9, 'name': 'Alert', 'phase': 'Phase 4: Information Sharing', 'days': [1, 2], 'partners': ['CERT']},
    {'seq': 10, 'name': 'Notify', 'phase': 'Phase 4: Information Sharing', 'days': [1, 17], 'partners': ['CERT', 'CLO', 'IT']},
    {'seq': 11, 'name': 'Plan', 'phase': 'Phase 5: Mitigation & Hardening', 'days': [2, 4], 'partners': ['CERT', 'IT', 'ENT']},
    {'seq': 12, 'name': 'Deploy', 'phase': 'Phase 5: Mitigation & Hardening', 'days': [2, 30], 'partners': ['IT', 'CSP', 'ENT']},
    {'seq': 13, 'name': 'Mitigate', 'phase': 'Phase 5: Mitigation & Hardening', 'days': [1, 30], 'partners': ['ENT', 'CLO', 'ISP']},
    {'seq': 14, 'name': 'Monitor', 'phase': 'Phase 5: Mitigation & Hardening', 'days': [1, 60], 'partners': ['CERT', 'ENT', 'CSP', 'CLO', 'THR', 'IT', 'ISP']},
    {'seq': 15, 'name': 'Review', 'phase': 'Phase 6: Learning & Improvement', 'days': [30, 60], 'partners': ['CERT']},
    {'seq': 16, 'name': 'Brief', 'phase': 'Phase 6: Learning & Improvement', 'days': [30, 60], 'partners': ['CERT']},
]

PARTNERS = ['CERT', 'CSP', 'CLO', 'IT', 'ENT', 'THR', 'ISP']
PHASES = ['Phase 1: Discovery & Assessment', 'Phase 2: Coordination', 
          'Phase 3: Detection & Intelligence', 'Phase 4: Information Sharing',
          'Phase 5: Mitigation & Hardening', 'Phase 6: Learning & Improvement']


def create_timeline():
    """Create a colorful timeline visualization showing actions and phases."""
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor(COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    # Calculate positions
    y_positions = {}
    phase_y = {}
    current_y = 0
    
    # Group actions by phase
    for phase in PHASES:
        phase_y[phase] = current_y
        phase_actions = [a for a in ACTIONS if a['phase'] == phase]
        for i, action in enumerate(phase_actions):
            y_positions[action['seq']] = current_y + i * 0.8
        current_y += len(phase_actions) * 0.8 + 1.5
    
    # Draw phase backgrounds
    for phase in PHASES:
        phase_actions = [a for a in ACTIONS if a['phase'] == phase]
        if phase_actions:
            min_y = min(y_positions[a['seq']] for a in phase_actions) - 0.4
            max_y = max(y_positions[a['seq']] for a in phase_actions) + 0.4
            ax.add_patch(FancyBboxPatch(
                (-0.5, min_y - 0.4), 36, max_y - min_y + 0.8,
                boxstyle="round,pad=0.1",
                facecolor=COLORS['phases'][phase],
                edgecolor='white',
                linewidth=2,
                alpha=0.15,
                zorder=0
            ))
            # Phase label
            ax.text(-1, (min_y + max_y) / 2, phase.split(':')[1].strip(), 
                   rotation=90, ha='center', va='center', fontsize=10, fontweight='bold',
                   color=COLORS['phases'][phase])
    
    # Draw timeline bars for each action
    for action in ACTIONS:
        y = y_positions[action['seq']]
        start_day = action['days'][0]
        end_day = action['days'][1]
        
        # Action bar
        color = COLORS['phases'][action['phase']]
        ax.barh(y, end_day - start_day, left=start_day, height=0.6, 
               color=color, alpha=0.7, edgecolor='white', linewidth=1.5, zorder=2)
        
        # Action label
        ax.text(start_day + (end_day - start_day) / 2, y, 
               f"{action['seq']}. {action['name']}", 
               ha='center', va='center', fontsize=8, fontweight='bold',
               color='white', zorder=3)
        
        # Partner icons/badges
        partner_x = end_day + 0.5
        for i, partner in enumerate(action['partners']):
            partner_color = COLORS['partners'][partner]
            circle = plt.Circle((partner_x + i * 0.4, y), 0.15, 
                              color=partner_color, zorder=3)
            ax.add_patch(circle)
            ax.text(partner_x + i * 0.4, y, partner, ha='center', va='center',
                   fontsize=6, color='white', fontweight='bold', zorder=4)
    
    # Customize axes
    ax.set_xlim(-3, 65)
    ax.set_ylim(-1, current_y + 1)
    ax.set_xlabel('Days Since Incident Start', fontsize=12, fontweight='bold', color=COLORS['text'])
    ax.set_title('Log4j Response Timeline: Actions and Partner Involvement', 
                fontsize=16, fontweight='bold', color=COLORS['text'], pad=20)
    ax.set_yticks([])
    ax.grid(True, alpha=0.3, axis='x')
    
    # Legend for partners
    legend_elements = [mpatches.Patch(facecolor=color, label=partner, edgecolor='white', linewidth=1)
                      for partner, color in COLORS['partners'].items()]
    ax.legend(handles=legend_elements, loc='upper right', title='Defensive Partners',
             frameon=True, fancybox=True, shadow=True)
    
    plt.tight_layout()
    plt.savefig('visualizations/log4j_timeline.png', facecolor=COLORS['background'], 
               bbox_inches='tight', edgecolor='none')
    print("✓ Created timeline visualization: visualizations/log4j_timeline.png")


def create_partner_matrix():
    """Create a heatmap showing partner involvement in each action."""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    # Build matrix
    matrix = np.zeros((len(PARTNERS), len(ACTIONS)))
    action_names = []
    
    for j, action in enumerate(ACTIONS):
        action_names.append(f"{action['seq']}. {action['name']}")
        for i, partner in enumerate(PARTNERS):
            if partner in action['partners']:
                # Weight by number of partners (more partners = more collaboration)
                matrix[i, j] = 1.0 + (len(action['partners']) - 1) * 0.1
    
    # Create heatmap with custom colors
    colors = ['#ffffff', '#e8f4f8', '#2E86AB', '#1a5f7a']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)
    
    sns.heatmap(matrix, annot=False, fmt='.0f', cmap=cmap, 
               cbar_kws={'label': 'Involvement Level', 'shrink': 0.8},
               xticklabels=action_names, yticklabels=PARTNERS,
               linewidths=0.5, linecolor='white', ax=ax)
    
    # Rotate labels
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    ax.set_title('Partner Involvement Matrix: Who Participates in Each Action',
                fontsize=16, fontweight='bold', color=COLORS['text'], pad=20)
    ax.set_xlabel('Collaboration Actions', fontsize=12, fontweight='bold', color=COLORS['text'])
    ax.set_ylabel('Defensive Partners', fontsize=12, fontweight='bold', color=COLORS['text'])
    
    # Add partner color indicators
    for i, partner in enumerate(PARTNERS):
        ax.add_patch(mpatches.Rectangle((-0.1, i), 0.05, 1, 
                                       facecolor=COLORS['partners'][partner],
                                       transform=ax.get_yaxis_transform(),
                                       clip_on=False))
    
    plt.tight_layout()
    plt.savefig('visualizations/log4j_partner_matrix.png', facecolor=COLORS['background'],
               bbox_inches='tight', edgecolor='none')
    print("✓ Created partner matrix: visualizations/log4j_partner_matrix.png")


def create_partner_capability_map():
    """Create a network diagram showing partner capabilities and relationships."""
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor(COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    # Partner positions in a circle
    angles = np.linspace(0, 2 * np.pi, len(PARTNERS), endpoint=False)
    radius = 3.5
    
    partner_pos = {}
    for i, partner in enumerate(PARTNERS):
        x = radius * np.cos(angles[i])
        y = radius * np.sin(angles[i])
        partner_pos[partner] = (x, y)
        
        # Draw partner node
        circle = plt.Circle((x, y), 0.4, facecolor=COLORS['partners'][partner],
                          edgecolor='white', linewidth=2, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, partner, ha='center', va='center', fontsize=10,
               fontweight='bold', color='white', zorder=4)
        
        # Partner label
        label_x = (radius + 0.8) * np.cos(angles[i])
        label_y = (radius + 0.8) * np.sin(angles[i])
        partner_names = {
            'CERT': 'National CSIRT',
            'CSP': 'Cybersecurity Service Provider',
            'CLO': 'Cloud Infrastructure Provider',
            'IT': 'Hardware/Software Vendor',
            'ENT': 'Mature Enterprise',
            'THR': 'Threat Intelligence Provider',
            'ISP': 'Internet Service Provider'
        }
        ax.text(label_x, label_y, partner_names[partner], ha='center', va='center',
               fontsize=8, color=COLORS['text'], fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                        edgecolor=COLORS['partners'][partner], linewidth=1.5))
    
    # Draw connections based on actions (partners that work together)
    partner_pairs = {}
    for action in ACTIONS:
        partners = action['partners']
        for i in range(len(partners)):
            for j in range(i + 1, len(partners)):
                pair = tuple(sorted([partners[i], partners[j]]))
                partner_pairs[pair] = partner_pairs.get(pair, 0) + 1
    
    # Draw edges with thickness based on frequency
    max_freq = max(partner_pairs.values()) if partner_pairs else 1
    for (p1, p2), freq in partner_pairs.items():
        x1, y1 = partner_pos[p1]
        x2, y2 = partner_pos[p2]
        
        # Line color based on average partner colors
        color1 = COLORS['partners'][p1]
        color2 = COLORS['partners'][p2]
        # Blend colors
        alpha = 0.3 + (freq / max_freq) * 0.4
        linewidth = 1 + (freq / max_freq) * 3
        
        ax.plot([x1, x2], [y1, y2], color='gray', alpha=alpha, 
               linewidth=linewidth, zorder=1)
    
    # Center coordinator (CERT)
    ax.plot(0, 0, 'o', markersize=20, color=COLORS['partners']['CERT'],
           markeredgecolor='white', markeredgewidth=3, zorder=5)
    ax.text(0, 0, 'CERT\nCoordinator', ha='center', va='center',
           fontsize=9, fontweight='bold', color='white', zorder=6)
    
    # Draw lines from CERT to all partners
    for partner in PARTNERS:
        if partner != 'CERT':
            x, y = partner_pos[partner]
            ax.plot([0, x], [0, y], color=COLORS['partners']['CERT'], 
                   alpha=0.2, linewidth=1.5, linestyle='--', zorder=1)
    
    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-5.5, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Partner Capability Network: Collaboration Relationships',
                fontsize=16, fontweight='bold', color=COLORS['text'], pad=20)
    
    # Add legend
    legend_text = "Line thickness indicates frequency of collaboration"
    ax.text(0, -5.2, legend_text, ha='center', fontsize=9, 
           style='italic', color=COLORS['text'])
    
    plt.tight_layout()
    plt.savefig('visualizations/log4j_partner_network.png', facecolor=COLORS['background'],
               bbox_inches='tight', edgecolor='none')
    print("✓ Created partner network: visualizations/log4j_partner_network.png")


def main():
    """Generate all visualizations."""
    import os
    os.makedirs('visualizations', exist_ok=True)
    
    print("Generating Log4j playbook visualizations...")
    print("=" * 60)
    
    create_timeline()
    create_partner_matrix()
    create_partner_capability_map()
    
    print("=" * 60)
    print("✓ All visualizations generated successfully!")
    print("\nGenerated files:")
    print("  - visualizations/log4j_timeline.png")
    print("  - visualizations/log4j_partner_matrix.png")
    print("  - visualizations/log4j_partner_network.png")


if __name__ == '__main__':
    main()

