#!/usr/bin/env python3
"""
Fretboard major-scale diagram with color-coded scale degrees.

- Fretboard is horizontal.
- High E string is at the TOP, low E at the BOTTOM.
- Major scale degrees are colored:
    1: red
    2: orange
    3: yellow
    4: green
    5: cyan
    6: blue
    7: purple
"""

from __future__ import annotations

from typing import Sequence
import argparse

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ===== CONFIG =============================================================

ROOT_NOTE = "A"  # Any of: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
FROM_FRET = 0  # Lowest fret to show
TO_FRET = 15  # Highest fret to show
SHOW_NOTE_NAMES = False  # True => show "degree\nnote", False => just degree

# Guitar tuning from TOP string to BOTTOM string in the diagram:
TUNING_TOP_TO_BOTTOM: Sequence[str] = ["E", "B", "G", "D", "A", "E"]

# ==========================================================================

NOTE_NAMES: Sequence[str] = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
]

# Allow common enharmonic spellings (flats, etc.)
ENHARMONIC_EQUIV: dict[str, str] = {
    "Cb": "B",
    "Db": "C#",
    "Eb": "D#",
    "Fb": "E",
    "Gb": "F#",
    "Ab": "G#",
    "Bb": "A#",
    "E#": "F",
    "B#": "C",
}

VALID_ROOTS = list(dict.fromkeys(list(NOTE_NAMES) + list(ENHARMONIC_EQUIV.keys())))

# Intervals of the major scale in semitones from the root
MAJOR_INTERVALS: Sequence[int] = [0, 2, 4, 5, 7, 9, 11]
MINOR_INTERVALS: Sequence[int] = [0, 2, 3, 5, 7, 8, 10]

DEGREE_TO_COLOR: dict[int, str] = {
    1: "#ff0000",
    2: "#ff8000",
    3: "#ffff00",
    4: "#00ff00",
    5: "#00ffff",
    6: "#0000ff",
    7: "#ff00ff",
}


def note_index(name: str) -> int:
    """
    Return chromatic index (0–11) for a note name like 'C#', 'Db', or 'F'.

    Accepts:
      - Naturals: C, D, E, F, G, A, B
      - Sharps:  C#, F#, etc.
      - Flats:   Db, Eb, Bb, etc.
      - Unicode accidentals: ♭, ♯
    """
    raw = name.strip()
    if not raw:
        raise ValueError("Empty note name")

    # Uppercase only the letter, keep accidental as-is
    letter = raw[0].upper()
    accidental = raw[1:]
    norm = letter + accidental  # e.g. "bb" -> "Bb"

    # Direct match (sharps / naturals in NOTE_NAMES)
    if norm in NOTE_NAMES:
        return NOTE_NAMES.index(norm)

    # Try enharmonic equivalents (flats, etc.)
    if norm in ENHARMONIC_EQUIV:
        canonical = ENHARMONIC_EQUIV[norm]
        return NOTE_NAMES.index(canonical)

    raise ValueError(f"Unknown note name {name!r}")


def build_scale(root: str, intervals: Sequence[int]) -> dict[int, int]:
    """
    Build mapping from chromatic index (0–11) to scale degree (1–7)
    for a given major scale root.
    """
    root_idx = note_index(root)
    mapping: dict[int, int] = {}
    for degree, step in enumerate(intervals, start=1):
        pitch_class = (root_idx + step) % 12
        mapping[pitch_class] = degree
    return mapping


def draw_scale_on_fretboard(
    root: str,
    intervals: Sequence[int],
    from_fret: int,
    to_fret: int,
    tuning_top_to_bottom: Sequence[str],
    show_note_names: bool = False,
    scale_name: str = "scale",
) -> None:
    """Draw a horizontal fretboard diagram with the given major scale."""
    scale_degrees = build_scale(root, intervals)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_facecolor("#f5f5f5")

    frets = list(range(from_fret, to_fret + 1))
    num_strings = len(tuning_top_to_bottom)

    # Draw frets (vertical lines)
    for i, fret in enumerate(frets):
        x = fret - from_fret
        if i != 0:
            ax.axvline(x, color="#bbbbbb", linewidth=1, zorder=1)
        ax.text(
            x,
            num_strings + 0.3,
            str(fret),
            ha="center",
            va="bottom",
            fontsize=8,
            zorder=3,
        )

    # Draw strings (horizontal lines) and labels
    for string_idx, open_note in enumerate(tuning_top_to_bottom):
        y = string_idx
        ax.axhline(y, color="#888888", linewidth=1.5, zorder=1)
        ax.text(
            -0.6,
            y,
            open_note,
            ha="right",
            va="center",
            fontsize=8,
            zorder=3,
        )

    # Draw notes that are in the major scale
    for string_idx, open_note in enumerate(tuning_top_to_bottom):
        open_pc = note_index(open_note)
        for fret in frets:
            note_pc = (open_pc + fret) % 12
            degree = scale_degrees.get(note_pc)
            if degree is None:
                continue  # not in the scale

            x = fret - from_fret
            y = string_idx
            color = DEGREE_TO_COLOR[degree]

            # Dot
            circle = Circle(
                (x, y),
                0.25,
                facecolor=color,
                edgecolor="black",
                linewidth=0.8,
                zorder=2,
            )
            ax.add_patch(circle)

            # Label on the dot
            if show_note_names:
                label = f"{degree}\n{NOTE_NAMES[note_pc]}"
            else:
                label = str(degree)

            ax.text(
                x,
                y,
                label,
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                zorder=3,
            )

    # Formatting: top string at top, bottom string at bottom
    ax.set_xlim(-1, len(frets))
    ax.set_ylim(-0.8, num_strings + 0.8)
    ax.invert_yaxis()
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_yticks([])

    top_string = tuning_top_to_bottom[0]
    bottom_string = tuning_top_to_bottom[-1]
    ax.set_title(
        f"{root} {scale_name} across strings\n"
        f"(high {top_string} on top, low {bottom_string} on bottom)"
    )

    # NOTE: no plt.show() here – we call it once at the end


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Draw major and natural minor scale diagrams on a guitar fretboard."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=ROOT_NOTE,
        choices=VALID_ROOTS,
        help=f"Root note name (default: {ROOT_NOTE})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.root

    draw_scale_on_fretboard(
        root=root,
        intervals=MAJOR_INTERVALS,
        from_fret=FROM_FRET,
        to_fret=TO_FRET,
        tuning_top_to_bottom=TUNING_TOP_TO_BOTTOM,
        show_note_names=SHOW_NOTE_NAMES,
        scale_name="major scale",
    )

    draw_scale_on_fretboard(
        root=root,
        intervals=MINOR_INTERVALS,
        from_fret=FROM_FRET,
        to_fret=TO_FRET,
        tuning_top_to_bottom=TUNING_TOP_TO_BOTTOM,
        show_note_names=SHOW_NOTE_NAMES,
        scale_name="natural minor scale",
    )

    plt.ion()  # Turn on interactive mode (just to be safe)
    plt.show(block=False)  # Don't block Python here

    try:
        # Keep the GUI responsive until all figures are closed
        while plt.get_fignums():
            plt.pause(0.1)  # Process GUI events
    except KeyboardInterrupt:
        print("\nCtrl-C detected, closing figures...")
        plt.close("all")


if __name__ == "__main__":
    main()
