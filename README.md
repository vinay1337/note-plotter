# Note Plotter

A visualization tool for guitar scales that generates color-coded fretboard diagrams using matplotlib.

## Features

- Creates clear, visual representations of scales on a guitar fretboard
- Supports both major and minor scales
- Color-codes each scale degree for easy recognition
- Configurable fret range (default: frets 0-15)
- Optional display of note names alongside scale degrees
- Customizable string tuning
- Interactive matplotlib display

## Installation

Clone this repository and install the requirements:

```bash
# Clone the repository
git clone https://github.com/yourusername/note-plotter.git
cd note-plotter

# Using uv (recommended)
uv sync
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Alternatively, using standard tools
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install .
```

## Usage

Run the main script to generate fretboard diagrams:

```bash
python main.py
```

This will open an interactive window with two diagrams:
1. The major scale in your configured root note
2. The natural minor scale in the same root note

The diagrams are interactive - you can zoom, pan, and save them using matplotlib's interface.

## Configuration

Edit the following variables at the top of `main.py` to customize the output:

```python
ROOT_NOTE = "A"  # Any of: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
FROM_FRET = 0  # Lowest fret to show
TO_FRET = 15  # Highest fret to show
SHOW_NOTE_NAMES = False  # True => show "degree\nnote", False => just degree

# Guitar tuning from TOP string to BOTTOM string in the diagram:
TUNING_TOP_TO_BOTTOM: Sequence[str] = ["E", "B", "G", "D", "A", "E"]
```

## Scale Degree Color Reference

Each scale degree is assigned a unique color for easy identification:

- 1 (Root): Red
- 2: Orange
- 3: Yellow
- 4: Green
- 5: Cyan
- 6: Blue
- 7: Purple

## Examples

When run with default settings (`ROOT_NOTE = "A"`), the tool produces two diagrams:
- A major scale across the fretboard
- A natural minor scale across the fretboard

The fretboard is displayed horizontally with the high E string at the top and the low E string at the bottom.

## Requirements

- Python 3.12+
