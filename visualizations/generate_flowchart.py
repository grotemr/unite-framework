#!/usr/bin/env python3
"""
Generate a flowchart visualization showing entities, actions, and artifacts
for the Log4j playbook. Focuses on the core detection-to-mitigation flow.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np

# Set style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 9

# Color scheme matching the main visualizations
COLORS = {
    'background': '#f8f9fa',
    'text': '#212529',
    'partners': {
        'CERT': '#2E86AB',
        'CSP': '#A23B72',
        'CLO': '#F18F01',
        'IT': '#C73E1D',
        'ENT': '#6A994E',
        'THR': '#BC4749',
        'ISP': '#219EBC'
    },
    'actions': '#4A90E2',  # Blue for action boxes
    'artifacts': '#95A5A6',  # Gray for documents/outputs
    'arrows': '#34495E'      # Dark gray for flow arrows
}

def create_flowchart():
    """Create a flowchart showing entities, actions, and artifacts."""
    fig, ax = plt.subplots(figsize=(18, 14))
    fig.patch.set_facecolor(COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    # Define the flow - focusing on core detection-to-mitigation sequence
    # Format: (entity, action, artifacts) - using Log4j-specific artifacts
    flow = [
        # Phase 1: Initial Discovery
        {
            'entities': ['CERT', 'IT', 'THR'],
            'action': 'Assess',
            'artifacts': ['CVE-2021-44228', 'RCE Vulnerability', 'Log4j 2.0-2.14.1'],
            'y': 12,
            'phase': 'Discovery'
        },
        {
            'entities': ['CERT'],
            'action': 'Prioritize',
            'artifacts': ['ED 22-02', '48hr timeline', 'CRITICAL priority'],
            'y': 10,
            'phase': 'Discovery'
        },
        {
            'entities': ['CERT'],
            'action': 'Partner',
            'artifacts': ['JCDC activated', 'Sharing channels', 'Partner list'],
            'y': 8,
            'phase': 'Coordination'
        },
        # Phase 2: Detection
        {
            'entities': ['ENT', 'CSP', 'CLO', 'THR'],
            'action': 'Hunt',
            'artifacts': ['${jndi:ldap://', '${jndi:dns://', 'Exploitation logs'],
            'y': 6,
            'phase': 'Detection'
        },
        {
            'entities': ['ENT', 'CSP', 'CLO', 'THR'],
            'action': 'Report',
            'artifacts': ['Sightings', 'Malicious domains', 'Time/Location'],
            'y': 4,
            'phase': 'Detection'
        },
        {
            'entities': ['CERT', 'THR', 'IT'],
            'action': 'Analyze',
            'artifacts': ['Attack TTPs', 'Infrastructure map', 'Exploit patterns'],
            'y': 2,
            'phase': 'Detection'
        },
        # Phase 3: Sharing & Mitigation
        {
            'entities': ['CERT', 'CSP', 'THR', 'IT'],
            'action': 'Share',
            'artifacts': ['CISA alerts', 'YARA rules', 'SIEM queries'],
            'y': 0,
            'phase': 'Sharing'
        },
        {
            'entities': ['IT', 'CSP', 'ENT'],
            'action': 'Deploy',
            'artifacts': ['Log4j 2.15.0+', 'JVM flags', 'WAF rules'],
            'y': -2,
            'phase': 'Mitigation'
        },
        {
            'entities': ['ENT', 'CLO', 'ISP'],
            'action': 'Mitigate',
            'artifacts': ['Patches applied', 'Domains blocked', 'Systems isolated'],
            'y': -4,
            'phase': 'Mitigation'
        }
    ]
    
    # Draw flowchart elements
    boxes = {}
    arrow_endpoints = {}
    
    for i, step in enumerate(flow):
        x = i * 2.2 + 1
        
        # Draw entity boxes (rounded rectangles at top)
        entity_y = step['y'] + 0.8
        entity_width = 0.35
        entity_spacing = 0.45
        
        entity_positions = {}
        for j, entity in enumerate(step['entities']):
            entity_x = x - (len(step['entities']) - 1) * entity_spacing / 2 + j * entity_spacing
            
            # Entity box
            entity_box = FancyBboxPatch(
                (entity_x - entity_width/2, entity_y - 0.2),
                entity_width, 0.4,
                boxstyle="round,pad=0.05",
                facecolor=COLORS['partners'][entity],
                edgecolor='white',
                linewidth=1.5,
                zorder=3
            )
            ax.add_patch(entity_box)
            
            # Entity label
            ax.text(entity_x, entity_y, entity, ha='center', va='center',
                   fontsize=8, fontweight='bold', color='white', zorder=4)
            
            entity_positions[entity] = (entity_x, entity_y)
            
            # Store for arrows
            if 'entities_box' not in boxes:
                boxes['entities_box'] = {}
            boxes['entities_box'][i] = (x, entity_y)
        
        # Draw action box (diamond shape)
        action_size = 0.6
        diamond_points = [
            (x, step['y'] + action_size/2),  # Top
            (x + action_size/2, step['y']),   # Right
            (x, step['y'] - action_size/2),    # Bottom
            (x - action_size/2, step['y'])    # Left
        ]
        action_diamond = mpatches.Polygon(diamond_points, 
                                         facecolor=COLORS['actions'],
                                         edgecolor='white',
                                         linewidth=2,
                                         zorder=3)
        ax.add_patch(action_diamond)
        
        # Action label
        ax.text(x, step['y'], step['action'], ha='center', va='center',
               fontsize=9, fontweight='bold', color='white', zorder=4,
               bbox=dict(boxstyle='round,pad=0.2', facecolor=COLORS['actions'],
                        edgecolor='white', linewidth=1.5, alpha=0.9))
        
        boxes[f'action_{i}'] = (x, step['y'])
        arrow_endpoints[i] = {'top': (x, step['y'] + action_size/2),
                             'bottom': (x, step['y'] - action_size/2)}
        
        # Draw artifact boxes (document shapes at bottom)
        artifact_y = step['y'] - 0.8
        artifact_width = 0.5
        artifact_height = 0.25
        
        artifact_positions = []
        for j, artifact in enumerate(step['artifacts']):
            artifact_x = x - (len(step['artifacts']) - 1) * artifact_width / 2 + j * artifact_width
            
            # Document shape (rounded rectangle with fold)
            doc_box = FancyBboxPatch(
                (artifact_x - artifact_width/2, artifact_y - artifact_height/2),
                artifact_width, artifact_height,
                boxstyle="round,pad=0.03",
                facecolor=COLORS['artifacts'],
                edgecolor='white',
                linewidth=1.5,
                zorder=3
            )
            ax.add_patch(doc_box)
            
            # Document fold (small triangle)
            fold_triangle = mpatches.Polygon([
                (artifact_x - artifact_width/2 + 0.05, artifact_y + artifact_height/2),
                (artifact_x - artifact_width/2 + 0.05, artifact_y + artifact_height/2 - 0.05),
                (artifact_x - artifact_width/2, artifact_y + artifact_height/2 - 0.05)
            ], facecolor='white', edgecolor=COLORS['artifacts'], linewidth=1, zorder=4)
            ax.add_patch(fold_triangle)
            
            # Artifact label
            ax.text(artifact_x, artifact_y, artifact, ha='center', va='center',
                   fontsize=7, color='white', fontweight='bold', zorder=5,
                   wrap=True)
            
            artifact_positions.append((artifact_x, artifact_y))
        
        boxes[f'artifacts_{i}'] = artifact_positions
        
        # Draw arrows from entities to action
        for entity_pos in entity_positions.values():
            arrow = FancyArrowPatch(
                (entity_pos[0], entity_pos[1] - 0.2),
                (x, step['y'] + action_size/2),
                arrowstyle='->', mutation_scale=15, linewidth=1.5,
                color=COLORS['arrows'], alpha=0.6, zorder=2
            )
            ax.add_patch(arrow)
        
        # Draw arrows from action to artifacts
        for artifact_pos in artifact_positions:
            arrow = FancyArrowPatch(
                (x, step['y'] - action_size/2),
                (artifact_pos[0], artifact_pos[1] + artifact_height/2),
                arrowstyle='->', mutation_scale=15, linewidth=1.5,
                color=COLORS['arrows'], alpha=0.6, zorder=2
            )
            ax.add_patch(arrow)
        
        # Draw flow arrows between actions (if not last)
        if i < len(flow) - 1:
            next_x = (i + 1) * 2.2 + 1
            next_y = flow[i + 1]['y']
            
            # Curved arrow from bottom of current action to top of next
            arrow = FancyArrowPatch(
                (x, step['y'] - action_size/2 - 0.3),
                (next_x, next_y + action_size/2 + 0.3),
                arrowstyle='->', mutation_scale=20, linewidth=2.5,
                color=COLORS['arrows'], alpha=0.8, zorder=2,
                connectionstyle="arc3,rad=0.3"
            )
            ax.add_patch(arrow)
    
    # Add phase labels with better positioning
    phase_labels = [
        (3.3, 11, 'Discovery', COLORS['phases']['Phase 1: Discovery & Assessment'] if 'phases' in COLORS else '#1f77b4'),
        (9.9, 5, 'Detection', COLORS['phases']['Phase 3: Detection & Intelligence'] if 'phases' in COLORS else '#2ca02c'),
        (16.5, -1, 'Sharing', COLORS['phases']['Phase 4: Information Sharing'] if 'phases' in COLORS else '#d62728'),
        (16.5, -3, 'Mitigation', COLORS['phases']['Phase 5: Mitigation & Hardening'] if 'phases' in COLORS else '#9467bd')
    ]
    
    for x, y, label, color in phase_labels:
        ax.add_patch(FancyBboxPatch(
            (x - 0.8, y - 0.3), 1.6, 0.6,
            boxstyle="round,pad=0.1",
            facecolor=color,
            edgecolor='white',
            linewidth=2,
            alpha=0.2,
            zorder=0
        ))
        ax.text(x, y, label, ha='center', va='center',
               fontsize=10, fontweight='bold', color=color, zorder=1)
    
    # Customize axes
    ax.set_xlim(-0.5, 19.8)
    ax.set_ylim(-5.5, 13.5)
    ax.axis('off')
    ax.set_title('Log4j Response Flowchart: Entities → Actions → Artifacts',
                fontsize=18, fontweight='bold', color=COLORS['text'], pad=20)
    
    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['partners']['CERT'], label='Defensive Partners', edgecolor='white'),
        mpatches.Patch(facecolor=COLORS['actions'], label='Collaboration Actions', edgecolor='white'),
        mpatches.Patch(facecolor=COLORS['artifacts'], label='Artifacts/Outputs', edgecolor='white'),
        mpatches.FancyArrowPatch((0, 0), (0.3, 0), arrowstyle='->', mutation_scale=15,
                               color=COLORS['arrows'], label='Flow Direction')
    ]
    ax.legend(handles=legend_elements, loc='upper right', frameon=True,
             fancybox=True, shadow=True, fontsize=9)
    
    # Add explanation text
    explanation = (
        "This flowchart shows a subset of the Log4j response focusing on core "
        "detection-to-mitigation activities. Defensive partners (entities) perform "
        "collaboration actions that produce specific artifacts/outputs, which feed "
        "into subsequent actions. Log4j-specific artifacts include JNDI patterns, "
        "CVE details, detection rules, and patches."
    )
    ax.text(9.9, -5.2, explanation, ha='center', va='top', fontsize=9, style='italic',
           color=COLORS['text'], wrap=True, bbox=dict(boxstyle='round,pad=0.5',
           facecolor='white', edgecolor=COLORS['artifacts'], linewidth=1.5))
    
    plt.tight_layout()
    plt.savefig('visualizations/log4j_flowchart.png', facecolor=COLORS['background'],
               bbox_inches='tight', edgecolor='none')
    print("✓ Created flowchart visualization: visualizations/log4j_flowchart.png")


if __name__ == '__main__':
    # Add phase colors for consistency
    COLORS['phases'] = {
        'Phase 1: Discovery & Assessment': '#1f77b4',
        'Phase 3: Detection & Intelligence': '#2ca02c',
        'Phase 4: Information Sharing': '#d62728',
        'Phase 5: Mitigation & Hardening': '#9467bd'
    }
    
    print("Generating Log4j flowchart visualization...")
    print("=" * 60)
    create_flowchart()
    print("=" * 60)
    print("✓ Flowchart visualization generated successfully!")

