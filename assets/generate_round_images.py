"""
Purpose: Generate three round-prompt visualization images for BBB project presentation.
         Each image shows a faded document on the left with highlighted excerpt regions,
         arrows connecting those highlights to magnified callout boxes on the right.
Author: Artist Agent
Date: 2026-03-29
Input: Static text excerpts from prompts/init_prompt.txt
Output: round1_prompt.png, round2_prompt.png, round3_prompt.png in ./assets/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import textwrap
import numpy as np

# ── Colour palette ──────────────────────────────────────────────────────────
AGENT_COLORS = {
    "Blacksmith": "#2E7D32",
    "Bookworm":   "#0077CC",
    "Artist":     "#6A1B9A",
    "Adversary":  "#C62828",
    "Conductor":  "#B8860B",
}

AGENT_LABELS = {
    "Blacksmith": "BLACKSMITH",
    "Bookworm":   "BOOKWORM",
    "Artist":     "ARTIST",
    "Adversary":  "ADVERSARY",
    "Conductor":  "CONDUCTOR",
}

AGENT_TINTS = {
    "Blacksmith": "#E8F5E9",
    "Bookworm":   "#E3F2FD",
    "Artist":     "#F3E5F5",
    "Adversary":  "#FFEBEE",
    "Conductor":  "#FFFDE7",
}

FONT = "DejaVu Sans"

# ── Round document texts (each line will be rendered individually) ────────
# Mark lines that should be highlighted with a tag: ##AGENT_NAME## at end

ROUND1_LINES = [
    ("This prompt is the first step to analyzing the", None),
    ("Blood Brain Barrier (BBB) dataset with respect", None),
    ("to Pin1. Please spawn all four subagents", None),
    ("simultaneously to work in parallel.", None),
    ("", None),
    ("BLACKSMITH:", None),
    ("Find and load the BBB dataset (Meng et al.,", None),
    ("PMID 34716354).", None),
    ("Write a Streamlit GUI to allow the user", "Blacksmith"),
    ("to explore the dataset. Allow the user to", "Blacksmith"),
    ("click on any molecule and see a graphical image.", "Blacksmith"),
    ("Show evidence — experimental vs. computational.", None),
    ("", None),
    ("BOOKWORM:", None),
    ("Create your literature survey and include", "Bookworm"),
    ("a specific section on Pin1 as a CNS drug target.", "Bookworm"),
    ("Note that Pin1 activators — not inhibitors", "Bookworm"),
    ("— may be neuroprotective.", "Bookworm"),
    ("", None),
    ("ARTIST:", None),
    ("Generate a series of images that describe", "Artist"),
    ("some basic statistics of the BBB dataset.", "Artist"),
    ("", None),
    ("ADVERSARY:", None),
    ("Critique the dataset from Meng and point out", "Adversary"),
    ("any weaknesses. Be very careful to distinguish", "Adversary"),
    ("between what you know and what you hypothesize.", "Adversary"),
    ("Also review the Artist's work.", None),
]

ROUND2_LINES = [
    ("BLACKSMITH:", None),
    ("Investigate whether any molecules have structural", None),
    ("features consistent with binding Pin1.", None),
    ("Two binding sites: WW domain and PPIase.", None),
    ("Fetch AlphaFold structure; run fpocket.", None),
    ("Screen ALL ~7,800 molecules for Tanimoto", "Blacksmith"),
    ("similarity (threshold 0.3). Report any", "Blacksmith"),
    ("molecule above threshold as a candidate.", "Blacksmith"),
    ("Run pharmacophore screening of BBB+ molecules.", None),
    ("", None),
    ("BOOKWORM:", None),
    ("Query ChEMBL for Pin1 inhibitors/activators", "Bookworm"),
    ("with CNS activity data. Query ClinicalTrials.gov", "Bookworm"),
    ("for Pin1 modulation trials in neurological disease.", "Bookworm"),
    ("Key papers: Lu 2003, Pastorino 2006.", None),
    ("Report whether any known activators are BBB+.", None),
    ("", None),
    ("ARTIST:", None),
    ("Fetch and render the AlphaFold structure of", "Artist"),
    ("Pin1 (P56399). Colour by pLDDT confidence score.", "Artist"),
    ("Highlight the WW domain and PPIase domain", "Artist"),
    ("in different colours.", "Artist"),
    ("", None),
    ("ADVERSARY:", None),
    ("Is the structural evidence for Pin1 binding", "Adversary"),
    ("convincing or speculative? Is the pLDDT", "Adversary"),
    ("confidence score high enough to trust", "Adversary"),
    ("a docking result?", "Adversary"),
    ("Risk of polypharmacology?", None),
]

ROUND3_LINES = [
    ("CONDUCTOR:", None),
    ("Using the findings of all subagents,", "Conductor"),
    ("write a short HTML report that highlights", "Conductor"),
    ("the most interesting findings and the", "Conductor"),
    ("most promising next steps.", "Conductor"),
    ("", None),
    ("CONDUCTOR:", None),
    ("Write an exam that tests the user's", "Conductor"),
    ("understanding of all material (technical,", "Conductor"),
    ("biological, background) that underlies", "Conductor"),
    ("our analysis here.", "Conductor"),
]

ROUND1_CALLOUTS = [
    ("Blacksmith",
     "Write a Streamlit GUI to allow the user to explore the dataset. "
     "Allow the user to click on any molecule and see a graphical image."),
    ("Bookworm",
     "Create your literature survey and include a specific section on Pin1... "
     "Note that Pin1 activators \u2014 not inhibitors \u2014 may be neuroprotective."),
    ("Artist",
     "Generate a series of images that describe some basic statistics of the BBB dataset."),
    ("Adversary",
     "Critique the dataset from Meng and point out any weaknesses... "
     "Be very careful to distinguish between what you know and what you hypothesize."),
]

ROUND2_CALLOUTS = [
    ("Blacksmith",
     "Screen ALL ~7,800 molecules using Morgan fingerprint Tanimoto similarity. "
     "Report any molecule above a threshold of 0.3 as a candidate."),
    ("Bookworm",
     "Query ChEMBL for all known Pin1 inhibitors and activators with CNS activity data. "
     "Query ClinicalTrials.gov for any trials involving Pin1 modulation."),
    ("Artist",
     "Fetch and render the AlphaFold structure of Pin1 (P56399). "
     "Colour by pLDDT confidence score. Highlight the WW domain and PPIase domain."),
    ("Adversary",
     "Is the structural evidence for Pin1 binding convincing or speculative? "
     "Is the pLDDT confidence score high enough to trust a docking result?"),
]

ROUND3_CALLOUTS = [
    ("Conductor",
     "Using the findings of all subagents, write a short HTML report that highlights "
     "the most interesting findings and the most promising next steps."),
    ("Conductor",
     "Write an exam that tests the user\u2019s understanding of all material \u2014 "
     "technical, biological, background \u2014 that underlies our analysis here."),
]


def draw_document_with_highlights(
    ax, lines: list, title: str,
    doc_x0: float, doc_y0: float, doc_w: float, doc_h: float,
) -> dict:
    """Draw document with per-line rendering. Returns dict mapping agent -> (mid_x, mid_y)
    for the center of highlighted region in axes coords."""

    # Drop shadow
    shadow = mpatches.FancyBboxPatch(
        (doc_x0 + 0.004, doc_y0 - 0.007), doc_w, doc_h,
        boxstyle="round,pad=0.004",
        linewidth=0, facecolor="#BBBBBB",
        transform=ax.transAxes, zorder=1, clip_on=False
    )
    ax.add_patch(shadow)

    # Page background
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
        linewidth=0, facecolor="#E0E0E0",
        transform=ax.transAxes, zorder=3, clip_on=False
    )
    ax.add_patch(title_bar)

    ax.text(doc_x0 + doc_w / 2, doc_y0 + doc_h - tb_h / 2, title,
            transform=ax.transAxes, zorder=4,
            ha="center", va="center",
            fontsize=10, fontweight="bold",
            fontfamily=FONT, color="#333333", clip_on=False)

    # Rule under title
    ax.plot([doc_x0, doc_x0 + doc_w],
            [doc_y0 + doc_h - tb_h, doc_y0 + doc_h - tb_h],
            color="#AAAAAA", lw=0.8, transform=ax.transAxes, zorder=4,
            clip_on=False)

    # Render lines individually
    margin_l = 0.012
    margin_t = 0.018
    line_h = 0.028  # height per line in axes fraction
    text_x = doc_x0 + margin_l
    start_y = doc_y0 + doc_h - tb_h - margin_t

    # Track highlighted regions per agent
    agent_line_ys: dict = {}  # agent -> list of y positions

    for i, (text, agent) in enumerate(lines):
        y = start_y - i * line_h

        if y < doc_y0 + 0.01:
            break  # don't draw below page

        if agent is not None:
            # Draw highlight rectangle
            color = AGENT_COLORS[agent]
            hl = mpatches.Rectangle(
                (doc_x0 + 0.004, y - line_h * 0.35),
                doc_w - 0.008, line_h * 0.85,
                linewidth=0,
                facecolor=color,
                alpha=0.15,
                transform=ax.transAxes, zorder=3, clip_on=False
            )
            ax.add_patch(hl)

            agent_line_ys.setdefault(agent, []).append(y)

            text_color = "#222222"
            text_alpha = 0.85
            fw = "normal"
        else:
            text_color = "#666666"
            text_alpha = 0.45
            fw = "normal"

        # Check if this is an agent header line
        if text and text.rstrip(":") in AGENT_COLORS:
            text_color = AGENT_COLORS[text.rstrip(":")]
            text_alpha = 0.70
            fw = "bold"

        ax.text(text_x, y, text,
                transform=ax.transAxes, zorder=5,
                ha="left", va="center",
                fontsize=7.0, fontfamily=FONT,
                fontweight=fw,
                color=text_color, alpha=text_alpha,
                clip_on=True)

    # Compute center of each agent's highlighted region
    highlight_centers = {}
    for agent, ys in agent_line_ys.items():
        mid_y = (max(ys) + min(ys)) / 2
        highlight_centers[agent] = (doc_x0 + doc_w, mid_y)

    return highlight_centers


def draw_callout(ax, agent: str, excerpt: str,
                 x0: float, y0: float, w: float, h: float):
    """Draw a single callout box. Returns left-center coords for arrow target."""
    color = AGENT_COLORS[agent]
    tint = AGENT_TINTS[agent]
    label = AGENT_LABELS[agent]

    # Shadow
    sh = mpatches.FancyBboxPatch(
        (x0 + 0.002, y0 - 0.004), w, h,
        boxstyle="round,pad=0.006",
        linewidth=0, facecolor="#DDDDDD",
        transform=ax.transAxes, zorder=2, clip_on=False
    )
    ax.add_patch(sh)

    # Background
    bg = mpatches.FancyBboxPatch(
        (x0, y0), w, h,
        boxstyle="round,pad=0.006",
        linewidth=1.2, edgecolor=color + "77",
        facecolor=tint,
        transform=ax.transAxes, zorder=3, clip_on=False
    )
    ax.add_patch(bg)

    # Left border stripe
    stripe_w = 0.007
    stripe = mpatches.Rectangle(
        (x0, y0), stripe_w, h,
        linewidth=0, facecolor=color,
        transform=ax.transAxes, zorder=4, clip_on=False
    )
    ax.add_patch(stripe)

    # Agent label
    ax.text(x0 + stripe_w + 0.010, y0 + h - 0.020, label,
            transform=ax.transAxes, zorder=5,
            ha="left", va="top",
            fontsize=11.5, fontweight="bold",
            fontfamily=FONT, color=color, clip_on=False)

    # Rule under label
    ax.plot([x0 + stripe_w + 0.008, x0 + w - 0.01],
            [y0 + h - 0.042, y0 + h - 0.042],
            color=color + "55", lw=0.8,
            transform=ax.transAxes, zorder=4, clip_on=False)

    # Excerpt text
    wrapped = textwrap.fill(excerpt, width=78)
    ax.text(x0 + stripe_w + 0.010, y0 + h - 0.050, wrapped,
            transform=ax.transAxes, zorder=5,
            ha="left", va="top",
            fontsize=10.8, fontfamily=FONT,
            color="#1A1A1A",
            linespacing=1.50, clip_on=False)

    return (x0, y0 + h / 2)


def draw_arrow(ax, start_xy: tuple, end_xy: tuple, color: str) -> None:
    """Draw a curved arrow from document highlight to callout box."""
    ax.annotate(
        "",
        xy=end_xy,
        xytext=start_xy,
        xycoords="axes fraction",
        textcoords="axes fraction",
        arrowprops=dict(
            arrowstyle="->,head_width=0.25,head_length=0.15",
            color=color,
            lw=1.8,
            connectionstyle="arc3,rad=0.15",
            alpha=0.7,
        ),
        zorder=6,
    )


def render_round(
    doc_lines: list, doc_title: str, callouts: list,
    output_path: str, is_short: bool = False,
    annotation: str = None,
) -> None:
    """Render a full 1920x900 round-prompt image."""
    dpi = 100
    fig, ax = plt.subplots(1, 1, figsize=(19.2, 9.0), dpi=dpi)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # ── Document dimensions ──
    doc_x0 = 0.028
    doc_w = 0.340
    if is_short:
        doc_h = 0.42
        doc_y0 = 0.48
    else:
        doc_h = 0.880
        doc_y0 = 0.060

    # Draw document with highlights; get highlight center positions
    highlight_centers = draw_document_with_highlights(
        ax, doc_lines, doc_title,
        doc_x0, doc_y0, doc_w, doc_h,
    )

    # ── Callout boxes ──
    n = len(callouts)
    right_x0 = 0.430
    right_w = 0.548
    pad_outer = 0.025
    pad_inner = 0.018
    total_h = 1.0 - 2 * pad_outer
    box_h = (total_h - pad_inner * (n - 1)) / n

    callout_centers = {}
    for i, (agent, excerpt) in enumerate(callouts):
        box_y0 = 1.0 - pad_outer - (i + 1) * box_h - i * pad_inner
        left_center = draw_callout(ax, agent, excerpt,
                                   right_x0, box_y0, right_w, box_h)
        # For Round 3 we have two Conductor entries; use index to distinguish
        key = f"{agent}_{i}" if agent == "Conductor" else agent
        callout_centers[key] = left_center

    # ── Draw arrows from highlight centers to callout left edges ──
    for i, (agent, _) in enumerate(callouts):
        key = f"{agent}_{i}" if agent == "Conductor" else agent
        color = AGENT_COLORS[agent]

        if agent in highlight_centers:
            start = highlight_centers[agent]
        else:
            # fallback: middle of document right edge
            start = (doc_x0 + doc_w, doc_y0 + doc_h / 2)

        end = callout_centers[key]
        draw_arrow(ax, start, end, color)

    # ── Bottom annotation (Round 3) ──
    if annotation:
        ann_y = 0.06
        pill = mpatches.FancyBboxPatch(
            (0.08, ann_y - 0.025), 0.84, 0.06,
            boxstyle="round,pad=0.010",
            linewidth=1.5, edgecolor="#4A148C55",
            facecolor="#F3E5F5",
            transform=ax.transAxes, zorder=5, clip_on=False
        )
        ax.add_patch(pill)
        ax.text(0.50, ann_y + 0.005, annotation,
                transform=ax.transAxes,
                ha="center", va="center",
                fontsize=22, fontweight="bold",
                fontfamily=FONT, color="#4A148C",
                zorder=6, clip_on=False)

    fig.savefig(output_path, dpi=dpi, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"  Saved: {output_path}")


# ── Execute ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    base = "/Users/mth/Desktop/bbb-project/assets"

    print("Rendering Round 1...")
    render_round(
        doc_lines=ROUND1_LINES,
        doc_title="Round 1 Prompt",
        callouts=ROUND1_CALLOUTS,
        output_path=f"{base}/round1_prompt.png",
    )

    print("Rendering Round 2...")
    render_round(
        doc_lines=ROUND2_LINES,
        doc_title="Round 2 Prompt",
        callouts=ROUND2_CALLOUTS,
        output_path=f"{base}/round2_prompt.png",
    )

    print("Rendering Round 3...")
    render_round(
        doc_lines=ROUND3_LINES,
        doc_title="Round 3 Prompt",
        callouts=ROUND3_CALLOUTS,
        output_path=f"{base}/round3_prompt.png",
        is_short=True,
        annotation="100% natural language instructions",
    )

    print("All three round images rendered successfully.")
