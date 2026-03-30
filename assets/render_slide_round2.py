"""
Purpose: Render a 1920x1080 presentation slide for Round 2 — Screen & Validate
Author: Artist Agent
Date: 2026-03-29
Input: None (hardcoded content)
Output: /Users/mth/Desktop/bbb-project/assets/slide_round2.png
"""

import textwrap

import matplotlib
matplotlib.use('Agg')
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Canvas: exactly 1920x1080 pixels
DPI = 100
FIG_W = 19.2   # inches  (19.2 * 100 = 1920 px)
FIG_H = 10.8   # inches  (10.8 * 100 = 1080 px)

fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])   # fill the whole figure
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis('off')
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# ── Colour palette ──────────────────────────────────────────────────────────
PURPLE_LABEL  = '#4A148C'
DARK_TITLE    = '#1a1a2e'
GREEN_SMITH   = '#2E7D32'
BLUE_WORM     = '#0077CC'
PURPLE_ARTIST = '#6A1B9A'
RED_ADV       = '#C62828'
CARD_BG       = '#F4F4F6'
BODY_GREY     = '#4A4A5A'

# ── Top label — fontsize doubled from 11.5 → 23 for clear prominence ────────
ax.text(
    FIG_W / 2, FIG_H - 0.75,
    'R O U N D   2   \u2014   S C R E E N   &   V A L I D A T E',
    ha='center', va='center',
    fontsize=23, fontweight='bold',
    color=PURPLE_LABEL,
    fontfamily='DejaVu Sans',
)

# ── Main title ───────────────────────────────────────────────────────────────
ax.text(
    FIG_W / 2, FIG_H - 1.65,
    'Hunting for Pin1 binders among BBB+ molecules',
    ha='center', va='center',
    fontsize=34, fontweight='bold',
    color=DARK_TITLE,
    fontfamily='DejaVu Sans',
)

# ── Layout constants ─────────────────────────────────────────────────────────
LEFT_M   = 1.05
RIGHT_M  = 1.05
GRID_TOP = FIG_H - 2.55    # top edge of the upper card row (shifted down slightly)
CARD_H   = 3.40
GAP_X    = 0.50
GAP_Y    = 0.38
TOTAL_W  = FIG_W - LEFT_M - RIGHT_M
CARD_W   = (TOTAL_W - GAP_X) / 2
BORDER_W = 0.09             # width of the coloured left accent bar

cards = [
    {
        'col': 0, 'row': 0,
        'agent': 'BLACKSMITH',
        'color': GREEN_SMITH,
        'body': (
            'Tanimoto similarity screen (~7,800 molecules) against known Pin1 ligands. '
            'Pharmacophore screening of BBB+ molecules against fpocket-identified '
            'binding pockets.'
        ),
    },
    {
        'col': 1, 'row': 0,
        'agent': 'BOOKWORM',
        'color': BLUE_WORM,
        'body': (
            'ChEMBL: Pin1 inhibitors/activators. ClinicalTrials.gov: CNS trials. '
            'Key papers (Lu 2003, Pastorino 2006). Any known activators BBB+?'
        ),
    },
    {
        'col': 0, 'row': 1,
        'agent': 'ARTIST',
        'color': PURPLE_ARTIST,
        'body': (
            'AlphaFold Pin1 structure coloured by pLDDT. Highlight WW & PPIase domains. '
            'Overlay candidate pharmacophores on binding pocket.'
        ),
    },
    {
        'col': 1, 'row': 1,
        'agent': 'ADVERSARY',
        'color': RED_ADV,
        'body': (
            'Binding evidence: convincing or speculative? AlphaFold confidence sufficient? '
            'Cancer tension: neuroprotective activator may be tumorigenic.'
        ),
    },
]

for card in cards:
    col   = card['col']
    row   = card['row']
    color = card['color']

    x0 = LEFT_M + col * (CARD_W + GAP_X)
    y0 = GRID_TOP - row * (CARD_H + GAP_Y) - CARD_H

    # ── Card background ──────────────────────────────────────────────────────
    bg = FancyBboxPatch(
        (x0, y0), CARD_W, CARD_H,
        boxstyle='round,pad=0.0',
        linewidth=0,
        facecolor=CARD_BG,
        zorder=2,
    )
    ax.add_patch(bg)

    # ── Coloured left accent bar ─────────────────────────────────────────────
    bar = patches.Rectangle(
        (x0, y0), BORDER_W, CARD_H,
        linewidth=0,
        facecolor=color,
        zorder=3,
    )
    ax.add_patch(bar)

    # ── Agent name ───────────────────────────────────────────────────────────
    text_x = x0 + BORDER_W + 0.30
    ax.text(
        text_x,
        y0 + CARD_H - 0.46,
        card['agent'],
        ha='left', va='top',
        fontsize=18, fontweight='bold',
        color=color,
        fontfamily='DejaVu Sans',
        zorder=4,
    )

    # ── Body text ────────────────────────────────────────────────────────────
    wrapped = textwrap.fill(card['body'], width=70)
    ax.text(
        text_x,
        y0 + CARD_H - 0.95,
        wrapped,
        ha='left', va='top',
        fontsize=14,
        color=BODY_GREY,
        fontfamily='DejaVu Sans',
        linespacing=1.6,
        zorder=4,
    )

# ── Save — exact 1920x1080 ────────────────────────────────────────────────────
out_path = '/Users/mth/Desktop/bbb-project/assets/slide_round2.png'
fig.savefig(out_path, dpi=DPI, bbox_inches=None, facecolor='white')
print(f'Saved: {out_path}')
plt.close(fig)
