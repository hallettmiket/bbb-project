"""
Purpose: Render a cinematic "Round 1 complete, puzzle pause" splash image
Author: ARTIST agent
Date: 2026-03-29
Output: /Users/mth/Desktop/bbb-project/assets/round1_puzzle_pause.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Arc, FancyArrowPatch, Wedge
import matplotlib.patheffects as pe
import numpy as np
import random

# ── Canvas ──────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
fig.patch.set_facecolor('#1a1a2e')
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.set_aspect('equal')
ax.axis('off')

rng = random.Random(42)
np_rng = np.random.RandomState(42)

# ── Background: subtle grid (chalkboard feel) ────────────────────────────────
for x in range(0, 1921, 60):
    ax.plot([x, x], [0, 1080], color='#16213e', linewidth=0.4, alpha=0.5, zorder=0)
for y in range(0, 1081, 60):
    ax.plot([0, 1920], [y, y], color='#16213e', linewidth=0.4, alpha=0.5, zorder=0)

# Vignette-like dark corners
for corner_x, corner_y in [(0, 0), (1920, 0), (0, 1080), (1920, 1080)]:
    for r, alpha in [(350, 0.18), (250, 0.12), (150, 0.07)]:
        c = Circle((corner_x, corner_y), r, color='#0a0a1a', alpha=alpha, zorder=1)
        ax.add_patch(c)

# ── TOP LEFT — ROUND 1 COMPLETE ─────────────────────────────────────────────
# Badge background
badge1 = FancyBboxPatch((40, 870), 340, 150,
                         boxstyle="round,pad=10",
                         facecolor='#0d2b0d', edgecolor='#2ecc71',
                         linewidth=3, zorder=5)
ax.add_patch(badge1)

ax.text(210, 980, "ROUND 1", fontsize=32, fontweight='bold',
        color='#2ecc71', ha='center', va='center', zorder=6,
        fontfamily='monospace')
ax.text(210, 935, "COMPLETE", fontsize=20, fontweight='bold',
        color='#27ae60', ha='center', va='center', zorder=6,
        fontfamily='monospace')

# Big green checkmark drawn with lines
ck_x, ck_y = 210, 895
ax.plot([ck_x - 18, ck_x - 5, ck_x + 22],
        [ck_y + 0, ck_y - 14, ck_y + 14],
        color='#2ecc71', linewidth=5, solid_capstyle='round',
        solid_joinstyle='round', zorder=7)

# Strike-through diagonal
ax.plot([50, 375], [870 + 150, 870], color='#2ecc71', linewidth=3,
        alpha=0.35, zorder=6, linestyle='--')

# ── TOP RIGHT — ROUND 2 LOCKED ──────────────────────────────────────────────
badge2 = FancyBboxPatch((1540, 870), 340, 150,
                         boxstyle="round,pad=10",
                         facecolor='#1c1c1c', edgecolor='#555555',
                         linewidth=3, zorder=5)
ax.add_patch(badge2)

ax.text(1710, 980, "ROUND 2", fontsize=32, fontweight='bold',
        color='#666666', ha='center', va='center', zorder=6,
        fontfamily='monospace')
ax.text(1710, 940, "NOT YET...", fontsize=16, fontweight='bold',
        color='#444444', ha='center', va='center', zorder=6,
        fontfamily='monospace',
        path_effects=[pe.withStroke(linewidth=2, foreground='#222222')])

# Padlock shape (drawn with patches)
lock_cx, lock_cy = 1710, 895
# shackle (arc)
shackle = Arc((lock_cx, lock_cy + 8), 22, 20, angle=0,
               theta1=0, theta2=180, color='#555555', linewidth=3.5, zorder=7)
ax.add_patch(shackle)
# body
lock_body = FancyBboxPatch((lock_cx - 14, lock_cy - 12), 28, 22,
                             boxstyle="round,pad=2",
                             facecolor='#444444', edgecolor='#666666',
                             linewidth=2, zorder=7)
ax.add_patch(lock_body)
# keyhole
keyhole_top = Circle((lock_cx, lock_cy - 2), 4.5, color='#1c1c1c', zorder=8)
ax.add_patch(keyhole_top)
ax.plot([lock_cx - 2, lock_cx + 2], [lock_cy - 6.5, lock_cy - 6.5],
        color='#1c1c1c', linewidth=4, zorder=8)

# ── CORK BOARD — CENTER EVIDENCE WALL ───────────────────────────────────────
board_x, board_y = 280, 180
board_w, board_h = 1360, 600

# Cork shadow
shadow = FancyBboxPatch((board_x + 10, board_y - 10), board_w, board_h,
                          boxstyle="round,pad=5",
                          facecolor='#000000', edgecolor='none', alpha=0.5,
                          zorder=4)
ax.add_patch(shadow)

# Cork board body
board = FancyBboxPatch((board_x, board_y), board_w, board_h,
                        boxstyle="round,pad=5",
                        facecolor='#c8a96e', edgecolor='#8b6914',
                        linewidth=5, zorder=5)
ax.add_patch(board)

# Cork texture — subtle noise dots
for _ in range(380):
    cx = rng.uniform(board_x + 15, board_x + board_w - 15)
    cy = rng.uniform(board_y + 15, board_y + board_h - 15)
    r = rng.uniform(1.5, 4.5)
    alpha = rng.uniform(0.08, 0.22)
    c = Circle((cx, cy), r, color='#7a5c2e', alpha=alpha, zorder=5)
    ax.add_patch(c)

# Board frame nails (corner pins)
for nx, ny in [(board_x + 18, board_y + board_h - 18),
               (board_x + board_w - 18, board_y + board_h - 18),
               (board_x + 18, board_y + 18),
               (board_x + board_w - 18, board_y + 18)]:
    nail = Circle((nx, ny), 7, color='#b8860b', zorder=8)
    ax.add_patch(nail)
    nail_shine = Circle((nx - 2, ny + 2), 2, color='#ffe066', alpha=0.6, zorder=9)
    ax.add_patch(nail_shine)

# ── STICKY NOTES ────────────────────────────────────────────────────────────
notes = [
    {
        'text': "Why does this\nmolecule look\nsuspicious??",
        'x': 340, 'y': 490, 'w': 195, 'h': 130,
        'color': '#fff176', 'tcolor': '#3e2723', 'angle': -4.5,
    },
    {
        'text': "These numbers\ndon't add up...",
        'x': 580, 'y': 520, 'w': 180, 'h': 110,
        'color': '#ffccbc', 'tcolor': '#4e342e', 'angle': 3.2,
    },
    {
        'text': "Pin1 activators?!\nREALLY??",
        'x': 820, 'y': 545, 'w': 175, 'h': 105,
        'color': '#c8e6c9', 'tcolor': '#1b5e20', 'angle': -2.8,
    },
    {
        'text': "Check the\nAdversary's notes",
        'x': 1060, 'y': 530, 'w': 185, 'h': 110,
        'color': '#ffcdd2', 'tcolor': '#b71c1c', 'angle': 4.1,
    },
    {
        'text': "Is the Bookworm\nhiding something?",
        'x': 1300, 'y': 510, 'w': 185, 'h': 115,
        'color': '#e1bee7', 'tcolor': '#4a148c', 'angle': -3.5,
    },
    # Upper row notes
    {
        'text': "AUC looks\ntoo good...",
        'x': 440, 'y': 330, 'w': 160, 'h': 100,
        'color': '#b3e5fc', 'tcolor': '#01579b', 'angle': 2.5,
    },
    {
        'text': "Data leakage?\nPossibly.",
        'x': 700, 'y': 295, 'w': 155, 'h': 110,
        'color': '#ffe0b2', 'tcolor': '#e65100', 'angle': -5.0,
    },
    {
        'text': "Molecule #447\n= FLAGGED",
        'x': 950, 'y': 310, 'w': 160, 'h': 100,
        'color': '#fce4ec', 'tcolor': '#880e4f', 'angle': 3.8,
    },
    {
        'text': "This scaffold\nappears TWICE",
        'x': 1180, 'y': 330, 'w': 165, 'h': 100,
        'color': '#f0f4c3', 'tcolor': '#33691e', 'angle': -2.2,
    },
]

# Draw red string connections first (behind notes)
string_connections = [
    (340 + 97, 490 + 65, 700 + 77, 295 + 55),
    (700 + 77, 295 + 55, 950 + 80, 310 + 50),
    (950 + 80, 310 + 50, 1060 + 92, 530 + 55),
    (580 + 90, 520 + 55, 820 + 87, 545 + 52),
    (820 + 87, 545 + 52, 1300 + 92, 510 + 57),
    (440 + 80, 330 + 50, 580 + 90, 520 + 55),
    (1180 + 82, 330 + 50, 1300 + 92, 510 + 57),
    (700 + 77, 295 + 55, 820 + 87, 545 + 52),
]

for x1, y1, x2, y2 in string_connections:
    # Slightly curved string using bezier-like waypoint
    mid_x = (x1 + x2) / 2 + rng.uniform(-20, 20)
    mid_y = (y1 + y2) / 2 + rng.uniform(-25, 15)
    xs = [x1, mid_x, x2]
    ys = [y1, mid_y, y2]
    ax.plot(xs, ys, color='#e53935', linewidth=1.6, alpha=0.75,
            zorder=6, solid_capstyle='round')

# Draw pins and notes
for note in notes:
    # Slight shadow
    shadow_note = FancyBboxPatch(
        (note['x'] + 4, note['y'] - 4), note['w'], note['h'],
        boxstyle="square,pad=2",
        facecolor='#000000', edgecolor='none', alpha=0.25,
        zorder=6,
        transform=matplotlib.transforms.Affine2D().rotate_deg_around(
            note['x'] + note['w']/2, note['y'] + note['h']/2, note['angle']
        ) + ax.transData
    )
    ax.add_patch(shadow_note)

    # Note body
    note_patch = FancyBboxPatch(
        (note['x'], note['y']), note['w'], note['h'],
        boxstyle="square,pad=2",
        facecolor=note['color'], edgecolor='#ccccaa',
        linewidth=1.2, zorder=7,
        transform=matplotlib.transforms.Affine2D().rotate_deg_around(
            note['x'] + note['w']/2, note['y'] + note['h']/2, note['angle']
        ) + ax.transData
    )
    ax.add_patch(note_patch)

    # Text on note (approximate center, not perfectly rotated but charming)
    tx = note['x'] + note['w'] / 2
    ty = note['y'] + note['h'] / 2
    ax.text(tx, ty, note['text'],
            fontsize=10.5, color=note['tcolor'],
            ha='center', va='center', zorder=8,
            fontweight='bold',
            rotation=note['angle'],
            linespacing=1.4)

    # Pin
    pin_x = note['x'] + note['w'] / 2
    pin_y = note['y'] + note['h'] - 8
    pin_circle = Circle((pin_x, pin_y), 6.5, color='#cc2200', zorder=9)
    ax.add_patch(pin_circle)
    pin_shine = Circle((pin_x - 1.5, pin_y + 1.5), 2.2, color='#ff6644',
                        alpha=0.7, zorder=10)
    ax.add_patch(pin_shine)

# ── QUESTION MARKS scattered on board ───────────────────────────────────────
qm_positions = [
    (310, 420, 36, '#cc8800', 0.65),
    (1490, 440, 42, '#cc3300', 0.55),
    (590, 230, 30, '#446600', 0.50),
    (1150, 260, 28, '#004488', 0.50),
    (760, 460, 24, '#770033', 0.45),
    (1420, 280, 22, '#333300', 0.40),
    (340, 260, 20, '#003344', 0.40),
]
for qx, qy, qsize, qcol, qalpha in qm_positions:
    ax.text(qx, qy, "?", fontsize=qsize, color=qcol, alpha=qalpha,
            ha='center', va='center', zorder=6,
            fontweight='bold', style='italic')

# ── MAGNIFYING GLASS — large, center-right of board ─────────────────────────
mg_cx, mg_cy = 1430, 430
mg_r = 85

# Glass body
glass_outer = Circle((mg_cx, mg_cy), mg_r, color='#2c1810', zorder=6)
ax.add_patch(glass_outer)
glass_ring = Circle((mg_cx, mg_cy), mg_r - 8, color='#5c3317', zorder=7)
ax.add_patch(glass_ring)
glass_inner = Circle((mg_cx, mg_cy), mg_r - 18, color='#aad4f5',
                      alpha=0.25, zorder=8)
ax.add_patch(glass_inner)
glass_lens = Circle((mg_cx, mg_cy), mg_r - 18, color='#88bbee',
                     alpha=0.10, zorder=8)
ax.add_patch(glass_lens)

# Lens glare
glare = Arc((mg_cx - 20, mg_cy + 22), 35, 20, angle=35,
             theta1=0, theta2=140, color='white', linewidth=2.5,
             alpha=0.45, zorder=9)
ax.add_patch(glare)

# Handle
handle_angle = -45
h_len = 110
hx1 = mg_cx + (mg_r - 5) * np.cos(np.radians(handle_angle + 180))
hy1 = mg_cy + (mg_r - 5) * np.sin(np.radians(handle_angle + 180))
hx2 = hx1 + h_len * np.cos(np.radians(handle_angle + 180))
hy2 = hy1 + h_len * np.sin(np.radians(handle_angle + 180))
ax.plot([hx1, hx2], [hy1, hy2], color='#3e1a00', linewidth=16,
        solid_capstyle='round', zorder=6)
ax.plot([hx1, hx2], [hy1, hy2], color='#6b3300', linewidth=10,
        solid_capstyle='round', zorder=7)

# Big "?" inside magnifying glass
ax.text(mg_cx, mg_cy + 4, "?", fontsize=55, color='#cc2200',
        ha='center', va='center', zorder=10, fontweight='bold',
        style='italic',
        path_effects=[pe.withStroke(linewidth=3, foreground='#1a0000')])

# ── TITLE — top center ───────────────────────────────────────────────────────
title_text = ax.text(960, 1040, "INTERMISSION",
                      fontsize=52, fontweight='bold',
                      color='#e8c84a', ha='center', va='center',
                      zorder=10, fontfamily='monospace',
                      path_effects=[
                          pe.withStroke(linewidth=6, foreground='#3d2b00'),
                          pe.Normal()
                      ])

# Subtitle
ax.text(960, 1000, "The investigation continues...",
        fontsize=18, color='#b8a040', ha='center', va='center',
        zorder=10, style='italic',
        path_effects=[pe.withStroke(linewidth=2, foreground='#1a1a2e')])

# ── BOTTOM TEXT ──────────────────────────────────────────────────────────────
ax.text(960, 130,
        "Hold on... let me think about this.",
        fontsize=38, color='#f5f5f5', ha='center', va='center',
        zorder=10, style='italic',
        fontfamily='DejaVu Sans',
        path_effects=[
            pe.withStroke(linewidth=5, foreground='#1a1a2e'),
            pe.Normal()
        ])

ax.text(960, 75,
        "Round 2 will wait.",
        fontsize=22, color='#888888', ha='center', va='center',
        zorder=10,
        fontfamily='monospace',
        path_effects=[pe.withStroke(linewidth=3, foreground='#1a1a2e')])

# ── POLICE TAPE STRIPS ───────────────────────────────────────────────────────
def draw_tape_strip(ax, x, y, width, height, angle, text, zorder=4):
    tape = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="square,pad=0",
        facecolor='#f0c800', edgecolor='#c0a000',
        linewidth=1.5, alpha=0.82, zorder=zorder,
        transform=matplotlib.transforms.Affine2D().rotate_deg_around(
            x + width/2, y + height/2, angle
        ) + ax.transData
    )
    ax.add_patch(tape)
    for i in range(0, int(width), 80):
        ax.text(x + i + 40, y + height/2, text,
                fontsize=8.5, color='#1a1a00', fontweight='bold',
                fontfamily='monospace', ha='center', va='center',
                alpha=0.70, zorder=zorder + 1,
                rotation=angle)

draw_tape_strip(ax, 0, 148, 1920, 24, 0, "INVESTIGATION IN PROGRESS  DO NOT CROSS  ", 3)
draw_tape_strip(ax, 0, 820, 1920, 22, 0, "CAUTION  PUZZLING DATA AHEAD  CAUTION  ", 3)

# ── FILM GRAIN overlay ───────────────────────────────────────────────────────
grain_x = np_rng.uniform(0, 1920, 3000)
grain_y = np_rng.uniform(0, 1080, 3000)
grain_s = np_rng.uniform(0.5, 2.5, 3000)
grain_a = np_rng.uniform(0.00, 0.06, 3000)
ax.scatter(grain_x, grain_y, s=grain_s, color='white', alpha=0.04,
           zorder=15, linewidths=0)

# ── SAVE ─────────────────────────────────────────────────────────────────────
out_path = "/Users/mth/Desktop/bbb-project/assets/round1_puzzle_pause.png"
fig.savefig(out_path, dpi=100, bbox_inches='tight',
            facecolor='#1a1a2e', pad_inches=0)
plt.close(fig)
print(f"Saved: {out_path}")
