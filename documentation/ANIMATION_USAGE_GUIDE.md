# NBA Movement Animation Script

Visualize NBA player movement data by generating MP4 animations from your CSV files. You can also export the official NBA court diagram as a static PNG.

Each frame shows all 10 players and the ball at a specific moment in time. The animation smoothly plays through every snapshot, creating smooth motion visualization.

## Quick Start

```bash
# Generate static NBA court diagram
python movement/animate_movement.py court

# Animate events 1-10
python movement/animate_movement.py animate data/csv/0021500492.csv --event-ids 1 10 --output animation.mp4

# Animate specific events with custom FPS
python movement/animate_movement.py animate data/csv/0021500492.csv --event-ids 1 3 5 --output animation.mp4 --fps 20

# Larger output with different figure size
python movement/animate_movement.py animate data/csv/0021500492.csv --event-ids 1 20 --output animation.mp4 --figsize 16 10
```

## Usage

```bash
python movement/animate_movement.py {animate,court} [OPTIONS]
```

### Commands

- `court`: Export the official NBA court diagram as PNG (nba_court.png)
- `animate`: Create animation from movement CSV data

### Animate Arguments

- `csv` (required): Path to movement CSV file

### Animate Options

- `--event-ids START END` or `--event-ids ID1 ID2 ID3 ...`: Event IDs to animate (default: 1 10)
  - Provide two numbers for a range: `--event-ids 5 20`
  - Provide multiple numbers for specific events: `--event-ids 1 5 10 15`

- `--output PATH`: Output MP4 file path (default: animation.mp4)

- `--fps INT`: Frames per second (default: 10)

- `--figsize WIDTH HEIGHT`: Figure size in inches (default: 14 8)

### Court Options

- `--output PATH`: Output PNG file path (default: nba_court.png)

- `--figsize WIDTH HEIGHT`: Figure size in inches (default: 14 8)

- `--dpi INT`: Resolution in dots per inch (default: 100)

## What's Visualized

### Court & Players

- **Court**: Official NBA court with all markings
- **Players**: Color-coded circles by team
  - Blue circles = Team 1 (1610612761)
  - Orange circles = Team 2 (1610612766)
- **Ball**: Black circle (slightly larger)

### Information Display

Each frame shows:
- **Event ID**: Display number of the event
- **Home Description**: Text description of the home team's action (blue text)
- **Visitor Description**: Text description of the visitor's action (orange text)
- **Possession Indicator**: Team with ball possession in top-right corner
- **Game Info**: Quarter, game clock, and shot clock

## Frame Count

Each event contains multiple snapshots taken at different game clock times. For example:
- Event 1 might have ~1,650 snapshots
- At 10 FPS, this creates a ~165 second animation showing smooth player movement
- Duplicate game clocks are removed (only the latest event shown at each timestamp)

## Examples

```bash
# Export the official NBA court diagram
python movement/animate_movement.py court
# Output: nba_court.png (1400x800 @ 100 DPI)

# Export court with higher resolution
python movement/animate_movement.py court --dpi 150 --output court_hires.png

# Animation of the opening possession (65 seconds video)
python movement/animate_movement.py animate data/csv/0021500492.csv --event-ids 1 2 --output opening.mp4 --fps 20

# Slow-motion replay of a single event
python movement/animate_movement.py animate data/csv/0021500492.csv --event-ids 5 5 --output single_event.mp4 --fps 10

# Fast-paced multiple events
python movement/animate_movement.py animate data/csv/0021500492.csv --event-ids 1 50 --output full_sequence.mp4 --fps 30
```

## Court Specifications

For detailed NBA court specifications and measurements, see [NBA_COURT_SPECS.md](NBA_COURT_SPECS.md).

### Key Dimensions

- **Court Size**: 94 ft (length) × 50 ft (width)
- **Basket Height**: 10 ft (vertical, not shown in 2D diagram)
- **Three-Point Distance**: 22-23.75 ft from basket (standardized since 1997-98 season)
- **Backboard to Rim**: 1.25 ft
- **Paint/Restricted Area**: 4 ft radius from basket
- **Free Throw Lane**: 16 ft wide × 19 ft deep

- pandas
- matplotlib
- numpy
- imageio-ffmpeg

Install with:
```bash
pip install pandas matplotlib numpy imageio imageio-ffmpeg
```

## Performance Notes

- Frames are rendered and encoded to MP4 in one pass
- Large ranges (100+ events) can take several minutes
- Output: 1152x688 @ H.264 codec for broad compatibility
- Possession labels loaded from events CSV if available

## Future Enhancements

Potential additions:
- Player trails/movement paths with transparency
- Interactive HTML animation with playback controls
- Player names/numbers overlay
- Zoom to specific court areas
- Custom color schemes per team
- Shot trajectory overlay

