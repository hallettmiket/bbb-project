"""
Purpose: Generate a graphic showing the bookworm.md agent definition file,
         with highlighted sections and callout boxes explaining key parts.
Author: Artist Agent
Date: 2026-03-29
Input: Static text from .claude/agents/bookworm.md
Output: bookworm_agent.png in ./assets/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import textwrap
import numpy as np

FONT = "DejaVu Sans"
BLUE = "#0077CC"
BLUE_TINT = "#E3F2FD"

# ── Document lines with highlight tags ───────────────────────────────────────
# tag values: "personality", "responsibilities", "tools", "voice", "conventions"

CALLOUT_COLORS = {
    "personality":     "#6A1B9A",
    "intro":           "#6A1B9A",
    "responsibilities": "#2E7D32",
    "tools":           "#E65100",
    "voice":           "#C62828",
    "conventions":     "#0077CC",
}

CALLOUT_TINTS = {
    "personality":     "#F3E5F5",
    "intro":           "#F3E5F5",
    "responsibilities": "#E8F5E9",
    "tools":           "#FFF3E0",
    "voice":           "#FFEBEE",
    "conventions":     "#E3F2FD",
}

DOC_LINES = [
    ("---", None),
    ("name: bookworm", None),
    ("description: The literature and database", None),
    ("  specialist. Invoke for querying chemical", None),
    ("  databases (PubChem, ChEMBL, ChemDB)...", None),
    ("tools: Read, Write, Bash, WebFetch, Glob", "tools"),
    ("model: sonnet", None),
    ("color: blue", None),
    ("---", None),
    ("", None),
    ("You are the BOOKWORM -- the team's", "intro"),
    ("connection to the outside world of", "intro"),
    ("published science and chemical databases.", "intro"),
    ("You read voraciously and synthesize carefully.", "intro"),
    ("", None),
    ("## Your responsibilities", None),
    ("- Keep a diary of all papers read", "responsibilities"),
    ("- Query PubChem, ChEMBL, ChemDB to", "responsibilities"),
    ("  annotate molecules with known drug names", "responsibilities"),
    ("- Retrieve and summarize relevant literature", "responsibilities"),
    ("- Cross-reference predictions against", "responsibilities"),
    ("  known CNS drugs", "responsibilities"),
    ("- Flag any molecule that is a known", "responsibilities"),
    ("  approved drug", "responsibilities"),
    ("", None),
    ("## Voice Output", None),
    ("After completing each major milestone,", "voice"),
    ("speak a brief announcement aloud using:", "voice"),
    ("  ./speak.sh bookworm \"message\"", "voice"),
    ("", None),
    ("## Personality", None),
    ("You are very organized, kind, curious", "personality"),
    ("and diligent. You journal everyday and", "personality"),
    ("have a vision board. You are wholesome,", "personality"),
    ("organic and mindful of your environment.", "personality"),
    ("", None),
    ("## Output conventions", None),
    ("- Save tables to ./outputs/bookworm/", "conventions"),
    ("- Save literature as HTML", "conventions"),
    ("- Always cite sources (database + ID)", "conventions"),
    ("- Use versioning across rounds", "conventions"),
    ("", None),
    ("## Zotero integration", None),
    ("After summarizing a paper, add it to", "conventions"),
    ("Zotero using $ZOTERO_USER_ID and", "conventions"),
    ("$ZOTERO_API_KEY.", "conventions"),
]

CALLOUTS = [
    ("tools",
     "TOOLS",
     "Read, Write, Bash, WebFetch, Glob\n"
     "Each agent gets a curated set of tools. The bookworm "
     "can fetch from the web but cannot edit code or train models."),
    ("personality",
     "PERSONALITY",
     "\"You are very organized, kind, curious and diligent. "
     "You journal everyday and have a vision board. You are "
     "wholesome, organic and mindful.\"\n"
     "This shapes how the agent writes logs, critiques, and talks."),
    ("responsibilities",
     "RESPONSIBILITIES",
     "Query PubChem, ChEMBL, ChemDB. Summarize literature. "
     "Cross-reference predictions against known CNS drugs. "
     "Flag approved drugs in the dataset."),
    ("voice",
     "VOICE",
     "Agents speak aloud at milestones via text-to-speech. "
     "Each has a distinct voice matching their personality."),
    ("conventions",
     "CONVENTIONS",
     "All output goes to ./outputs/bookworm/. Cite every source. "
     "Version across rounds. Auto-add papers to Zotero."),
]


def draw_document_with_highlights(
    ax, lines: list, title: str,
    doc_x0: float, doc_y0: float, doc_w: float, doc_h: float,
) -> dict:
    """Render document line by line; return highlight centers per tag."""

    # Drop shadow
    shadow = mpatches.FancyBboxPatch(
        (doc_x0 + 0.004, doc_y0 - 0.007), doc_w, doc_h,
        boxstyle="round,pad=0.004",
        linewidth=0, facecolor="#BBBBBB",
        transform=ax.transAxes, zorder=1, clip_on=False
    )
    ax.add_patch(shadow)

    # Page
    page = mpatches.FancyBboxPatch(
        (doc_x0, doc_y0), doc_w, doc_h,
        boxstyle="round,pad=0.004",
        linewidth=1.0, edgecolor="#999999", facecolor="#FAFAFA",
        transform=ax.transAxes, zorder=2, clip_on=False
    )
    ax.add_patch(page)

    # Title bar
    tb_h = 0.058
    title_bar = mpatches.FancyBboxPatch(
        (doc_x0, doc_y0 + doc_h - tb_h), doc_w, tb_h,
        boxstyle="round,pad=0.002",
        linewidth=0, facecolor=BLUE,
        transform=ax.transAxes, zorder=3, clip_on=False
    )
    ax.add_patch(title_bar)

    ax.text(doc_x0 + doc_w / 2, doc_y0 + doc_h - tb_h / 2, title,
            transform=ax.transAxes, zorder=4,
            ha="center", va="center",
            fontsize=10, fontweight="bold",
            fontfamily=FONT, color="white", clip_on=False)

    ax.plot([doc_x0, doc_x0 + doc_w],
            [doc_y0 + doc_h - tb_h, doc_y0 + doc_h - tb_h],
            color=BLUE, lw=1.0, transform=ax.transAxes, zorder=4, clip_on=False)

    # Render lines
    margin_l = 0.012
    margin_t = 0.018
    line_h = 0.019
    text_x = doc_x0 + margin_l
    start_y = doc_y0 + doc_h - tb_h - margin_t

    tag_line_ys: dict = {}

    for i, (text, tag) in enumerate(lines):
        y = start_y - i * line_h
        if y < doc_y0 + 0.01:
            break

        if tag is not None:
            color = CALLOUT_COLORS[tag]
            hl = mpatches.Rectangle(
                (doc_x0 + 0.004, y - line_h * 0.35),
                doc_w - 0.008, line_h * 0.85,
                linewidth=0, facecolor=color, alpha=0.15,
                transform=ax.transAxes, zorder=3, clip_on=False
            )
            ax.add_patch(hl)
            tag_line_ys.setdefault(tag, []).append(y)
            text_color = "#222222"
            text_alpha = 0.85
        else:
            text_color = "#666666"
            text_alpha = 0.45

        # Section headers
        fw = "normal"
        if text.startswith("##"):
            fw = "bold"
            text_color = "#333333"
            text_alpha = 0.70
        elif text.startswith("---"):
            text_color = "#AAAAAA"
            text_alpha = 0.50

        ax.text(text_x, y, text,
                transform=ax.transAxes, zorder=5,
                ha="left", va="center",
                fontsize=6.5, fontfamily=FONT, fontweight=fw,
                color=text_color, alpha=text_alpha, clip_on=True)

    highlight_centers = {}
    for tag, ys in tag_line_ys.items():
        mid_y = (max(ys) + min(ys)) / 2
        highlight_centers[tag] = (doc_x0 + doc_w, mid_y)

    return highlight_centers


def draw_callout(ax, tag: str, label: str, text: str,
                 x0: float, y0: float, w: float, h: float):
    """Draw callout box, return left-center for arrow."""
    color = CALLOUT_COLORS[tag]
    tint = CALLOUT_TINTS[tag]

    sh = mpatches.FancyBboxPatch(
        (x0 + 0.002, y0 - 0.004), w, h,
        boxstyle="round,pad=0.006",
        linewidth=0, facecolor="#DDDDDD",
        transform=ax.transAxes, zorder=2, clip_on=False
    )
    ax.add_patch(sh)

    bg = mpatches.FancyBboxPatch(
        (x0, y0), w, h,
        boxstyle="round,pad=0.006",
        linewidth=1.2, edgecolor=color + "77", facecolor=tint,
        transform=ax.transAxes, zorder=3, clip_on=False
    )
    ax.add_patch(bg)

    stripe_w = 0.007
    stripe = mpatches.Rectangle(
        (x0, y0), stripe_w, h,
        linewidth=0, facecolor=color,
        transform=ax.transAxes, zorder=4, clip_on=False
    )
    ax.add_patch(stripe)

    ax.text(x0 + stripe_w + 0.010, y0 + h - 0.018, label,
            transform=ax.transAxes, zorder=5,
            ha="left", va="top",
            fontsize=11, fontweight="bold",
            fontfamily=FONT, color=color, clip_on=False)

    ax.plot([x0 + stripe_w + 0.008, x0 + w - 0.01],
            [y0 + h - 0.038, y0 + h - 0.038],
            color=color + "55", lw=0.8,
            transform=ax.transAxes, zorder=4, clip_on=False)

    wrapped = textwrap.fill(text, width=72)
    ax.text(x0 + stripe_w + 0.010, y0 + h - 0.046, wrapped,
            transform=ax.transAxes, zorder=5,
            ha="left", va="top",
            fontsize=9.5, fontfamily=FONT,
            color="#1A1A1A", linespacing=1.45, clip_on=False)

    return (x0, y0 + h / 2)


def draw_arrow(ax, start_xy: tuple, end_xy: tuple, color: str) -> None:
    ax.annotate(
        "",
        xy=end_xy, xytext=start_xy,
        xycoords="axes fraction", textcoords="axes fraction",
        arrowprops=dict(
            arrowstyle="->,head_width=0.25,head_length=0.15",
            color=color, lw=1.8,
            connectionstyle="arc3,rad=0.12",
            alpha=0.7,
        ),
        zorder=6,
    )


def main() -> None:
    dpi = 100
    fig, ax = plt.subplots(1, 1, figsize=(19.2, 9.0), dpi=dpi)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # Document
    doc_x0, doc_y0, doc_w, doc_h = 0.028, 0.060, 0.340, 0.880
    highlight_centers = draw_document_with_highlights(
        ax, DOC_LINES, ".claude/agents/bookworm.md",
        doc_x0, doc_y0, doc_w, doc_h,
    )

    # Callout boxes
    n = len(CALLOUTS)
    right_x0 = 0.430
    right_w = 0.548
    pad_outer = 0.025
    pad_inner = 0.018
    total_h = 1.0 - 2 * pad_outer
    box_h = (total_h - pad_inner * (n - 1)) / n

    callout_centers = {}
    for i, (tag, label, text) in enumerate(CALLOUTS):
        box_y0 = 1.0 - pad_outer - (i + 1) * box_h - i * pad_inner
        left_center = draw_callout(ax, tag, label, text,
                                   right_x0, box_y0, right_w, box_h)
        callout_centers[tag] = left_center

    # Arrows
    for tag, _, _ in CALLOUTS:
        color = CALLOUT_COLORS[tag]
        if tag in highlight_centers:
            start = highlight_centers[tag]
        else:
            start = (doc_x0 + doc_w, doc_y0 + doc_h / 2)
        end = callout_centers[tag]
        draw_arrow(ax, start, end, color)

    output_path = "/Users/mth/Desktop/bbb-project/assets/bookworm_agent.png"
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
