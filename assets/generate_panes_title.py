"""
Purpose: Generate the full-screen desktop background for the demo display.
Author: Claude
Date: 2026-03-21
Input: None
Output: assets/panes_title_by_characters.jpeg

Layout (matches start_demo.sh):
  Left 42%:  VSCode (Conductor)
  2% gap
  44-98%:    4 agent windows stacked vertically (each 25% of full height)
  Right 2%:  agent name labels (vertical text)

Agent names are placed in the right margin after the agent windows,
vertically aligned with each agent's row.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# 4K resolution (2x retina of 1920x1080 logical)
WIDTH = 3840
HEIGHT = 2160

# Layout percentages (must match start_demo.sh)
MENU_BAR_PX = 25 * 2  # 25 logical points * 2x retina
VSCODE_RIGHT_PCT = 42
AGENT_LEFT_PCT = 44
AGENT_RIGHT_PCT = 98

# Usable height for agents (from menu bar to bottom — matches VSCode height)
AGENT_TOP = MENU_BAR_PX
AGENT_BOTTOM = HEIGHT
USABLE_HEIGHT = AGENT_BOTTOM - AGENT_TOP

AGENTS = [
    {"name": "BLACKSMITH", "emoji": "⚒", "color": (0, 255, 0)},
    {"name": "BOOKWORM", "emoji": "📚", "color": (0, 128, 255)},
    {"name": "ARTIST", "emoji": "🎨", "color": (255, 0, 255)},
    {"name": "ADVERSARY", "emoji": "⚔", "color": (255, 0, 0)},
]

img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(img)

# Larger font for vertical agent names
try:
    font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 36)
except OSError:
    font = ImageFont.load_default()

# Right margin: 98%-100% of screen width
agent_right_px = int(WIDTH * AGENT_RIGHT_PCT / 100)
margin_center_x = (agent_right_px + WIDTH) // 2

# Colored accent line width
accent_width = 4

for i, agent in enumerate(AGENTS):
    row_top = AGENT_TOP + USABLE_HEIGHT * i // 4
    row_bottom = AGENT_TOP + USABLE_HEIGHT * (i + 1) // 4
    row_center_y = (row_top + row_bottom) // 2

    # Colored accent line on the right edge of the agent window area
    draw.rectangle(
        [agent_right_px + 1, row_top + 2, agent_right_px + accent_width, row_bottom - 2],
        fill=agent["color"],
    )

    # Render text horizontally on a temporary image, then rotate 90° CCW
    label = agent["name"]
    bbox = draw.textbbox((0, 0), label, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    txt_img = Image.new("RGBA", (text_w + 4, text_h + 4), (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_img)
    txt_draw.text((-bbox[0] + 2, -bbox[1] + 2), label, fill=agent["color"], font=font)

    # Rotate 90° clockwise (text reads top-to-bottom)
    rotated = txt_img.rotate(-90, expand=True)

    # Paste rotated text centered in the right margin, vertically in the row
    paste_x = margin_center_x - rotated.width // 2
    paste_y = row_center_y - rotated.height // 2
    img.paste(rotated, (paste_x, paste_y), rotated)

output_path = Path(__file__).parent / "panes_title_by_characters.jpeg"
img.save(output_path, "JPEG", quality=95)
print(f"Saved {output_path} ({WIDTH}x{HEIGHT})")
