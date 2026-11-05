#!/usr/bin/env python3
"""
Animate NBA player movement data to MP4 video using PIL for fast frame composition.
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import imageio.v2 as imageio
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io
import time

from court import draw_court, COURT_LENGTH, COURT_WIDTH

# Color mapping for teams
TEAM_COLORS = {
    1610612761: '#1f77b4',  # Blue
    1610612766: '#ff7f0e',  # Orange
    -1: 'black'  # Ball
}

def validate_game(df):
    """Validate that the game has exactly two teams (excluding the ball)."""
    
    if len(df['event_id'].unique()) == 0:
            print("No events found in the filtered data.")
            return False
    
    team_list = [t for t in df['team_id'].unique() if t != -1]
    if len(team_list) != 2:
        print("Too many or too few teams found. Not a valid game")
        return False
    return True


def dedupe_frames(df):
    frames_data = []
    unique_times = sorted(df['game_clock'].unique(), reverse=True)
    
    for game_clock in unique_times:
        # Get all rows at this exact timestamp across all events
        frame_data = df[df['game_clock'] == game_clock]
        # Get all event IDs that have data at this timestamp
        applicable_events = sorted(frame_data['event_id'].unique())
        frames_data.append((applicable_events, game_clock, frame_data))
    
    return frames_data


def find_marker_in_image(img_array, target_color, tolerance=30):
    """Find center of pixels matching a target color in image array.
    
    Args:
        img_array: numpy array of shape (height, width, 3) in RGB
        target_color: tuple (r, g, b) to search for
        tolerance: color tolerance (how close each channel must be)
    
    Returns:
        tuple: (pixel_x, pixel_y) center of matching region, or None if not found
    """
    r, g, b = target_color
    # Find all pixels close to target color
    mask = (
        (np.abs(img_array[:,:,0].astype(int) - r) < tolerance) &
        (np.abs(img_array[:,:,1].astype(int) - g) < tolerance) &
        (np.abs(img_array[:,:,2].astype(int) - b) < tolerance)
    )
    
    if not mask.any():
        return None
    
    # Get center of mass
    y_coords, x_coords = np.where(mask)
    center_x = x_coords.mean()
    center_y = y_coords.mean()
    return (center_x, center_y)


def load_event_data(csv_path, event_ids):
    """Load and filter movement data for specified event IDs."""
    df = pd.read_csv(csv_path)
    
    if isinstance(event_ids, list):
        if len(event_ids) == 2:
            # Range provided as [start, end]
            filtered = df[(df['event_id'] >= event_ids[0]) & (df['event_id'] <= event_ids[1])]
        else:
            # Explicit list of event IDs
            filtered = df[df['event_id'].isin(event_ids)]
    else:
        filtered = df[df['event_id'] == event_ids]
    
    # Sort by event_id and game_clock for proper sequencing
    filtered = filtered.sort_values(['event_id', 'game_clock'], ascending=[True, False])
    return filtered


def create_court_background_image(figsize=(12, 8), dpi=48):
    """Create court background image and automatically measure coordinate mapping.
    
    Renders the court with calibration markers at the exact court corners (0,0), (94,0), 
    (0,50), (94,50), then scans the image to find their pixel positions.
    Uses these to calculate the precise coordinate transformation.
    
    Returns:
        tuple: (PIL Image, x_scale, y_scale, x_offset, y_offset)
               where pixel_x = court_x * x_scale + x_offset
                     pixel_y = court_y * y_scale + y_offset
    """
    # Step 1: Render with markers to measure mapping
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_position([0, 0, 1, 1])
    draw_court(ax)
    
    # Render to PIL Image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches=None, pad_inches=0, dpi=dpi)
    buf.seek(0)
    marked_img = Image.open(buf).convert('RGB')
    img_array = np.array(marked_img)
    
    plt.close(fig)
    
    # Step 2: Find marker positions in the rendered image
    markers = {}
    marker_colors = [
        ((0, 0), (255, 0, 255)),      # Magenta at court (0, 0)
        ((COURT_LENGTH, 0), (0, 255, 0)),     # Green at court (94, 0)
        ((0, COURT_WIDTH), (0, 0, 255)),      # Blue at court (0, 50)
        ((COURT_LENGTH, COURT_WIDTH), (255, 255, 0)),  # Yellow at court (94, 50)
    ]
    
    for court_coord, rgb_color in marker_colors:
        pixel_pos = find_marker_in_image(img_array, rgb_color, tolerance=40)
        if pixel_pos:
            markers[court_coord] = pixel_pos
            print(f"  Marker at court {court_coord} found at pixel {pixel_pos}")
        else:
            print(f"  WARNING: Marker at court {court_coord} not found!")
    
    if len(markers) < 2:
        raise RuntimeError("Failed to find enough calibration markers in rendered image")
    
    # Step 3: Calculate transformation from markers
    if (0, 0) in markers and (COURT_LENGTH, COURT_WIDTH) in markers:
        px_0_0, py_0_0 = markers[(0, 0)]
        px_94_50, py_94_50 = markers[(COURT_LENGTH, COURT_WIDTH)]
        
        x_scale = (px_94_50 - px_0_0) / COURT_LENGTH
        y_scale = (py_94_50 - py_0_0) / COURT_WIDTH
        x_offset = px_0_0
        y_offset = py_0_0
    else:
        # Fallback calculation
        items = list(markers.items())
        (cx1, cy1), (px1, py1) = items[0]
        (cx2, cy2), (px2, py2) = items[1]
        
        if cx2 != cx1:
            x_scale = (px2 - px1) / (cx2 - cx1)
            x_offset = px1 - cx1 * x_scale
        else:
            x_scale = 1.0
            x_offset = px1
        
        if cy2 != cy1:
            y_scale = (py2 - py1) / (cy2 - cy1)
            y_offset = py1 - cy1 * y_scale
        else:
            y_scale = 1.0
            y_offset = py1
    
    print(f"  Calculated: x_scale={x_scale:.4f} px/unit, y_scale={y_scale:.4f} px/unit")
    print(f"  Offset: x={x_offset:.2f}, y={y_offset:.2f}")
    
    # Step 4: Render clean background (no markers) for use in frames
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_position([0, 0, 1, 1])
    draw_court(ax, markers=False)
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches=None, pad_inches=0, dpi=dpi)
    buf.seek(0)
    court_img_clean = Image.open(buf).convert('RGB')
    plt.close(fig)
    
    return court_img_clean, x_scale, y_scale, x_offset, y_offset


def hex_to_rgb(color):
    """Convert hex color string or named color to RGB tuple."""
    # Map named colors
    named_colors = {
        'black': (0, 0, 0),
        'gray': (128, 128, 128),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'blue': (0, 0, 255),
    }
    
    if color in named_colors:
        return named_colors[color]
    
    # Handle hex colors
    hex_color = color.lstrip('#')
    if len(hex_color) != 6:
        return (128, 128, 128)  # Default to gray if invalid
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def draw_circle_with_border(draw, x, y, radius, fill_color, border_color, border_width=1):
    """Draw a circle with a border using PIL."""
    # Draw filled circle
    bbox = [x - radius, y - radius, x + radius, y + radius]
    draw.ellipse(bbox, fill=fill_color, outline=border_color, width=border_width)


def compose_frame_pil(background_img, positions_at_time, colors_at_time, 
                      sizes_at_time, event_text, info_text, x_scale, y_scale, x_offset, y_offset,
                      padding_bottom=96, padding_top=80):
    """Compose a single frame by overlaying scatter points on background image.
    
    Uses pre-calculated coordinate mapping from court space to pixel space.
    Creates a larger canvas with padding for text outside the court background.
    Returns numpy array suitable for imageio.
    
    Args:
        padding_bottom: pixels to add below the court for info text (default 96, divisible by 16)
        padding_top: pixels to add above the court for title text (default 80, divisible by 16)
    """
    # Create larger canvas with padding (maintain divisibility by 16)
    canvas_width = background_img.width
    canvas_height = background_img.height + padding_top + padding_bottom
    canvas = Image.new('RGB', (canvas_width, canvas_height), color='white')
    
    # Paste background image in center (with top padding)
    canvas.paste(background_img, (0, padding_top))
    
    draw = ImageDraw.Draw(canvas)
    
    # Draw scatter points using coordinate mapping
    for pos, color, size in zip(positions_at_time, colors_at_time, sizes_at_time):
        court_x, court_y = pos
        
        # Map court coordinates to pixel coordinates
        pixel_x = court_x * x_scale + x_offset
        # Adjust y coordinate for top padding
        pixel_y = court_y * y_scale + y_offset + padding_top
        
        # Convert matplotlib scatter size to pixel radius
        # size 200 for players, size 300 for ball
        pixel_radius = int(np.sqrt(size / np.pi))
        
        # Convert color
        rgb_color = hex_to_rgb(color)
        
        # Draw circle with border
        draw_circle_with_border(draw, pixel_x, pixel_y, pixel_radius, 
                               fill_color=rgb_color, border_color=(0, 0, 0), border_width=2)
    
    # Add text overlays
    title_font = ImageFont.load_default(size=32)
    info_font = ImageFont.load_default(size=24)
    
    # Draw title text (event IDs) in top padding area, with vertical centering
    title_bbox = draw.textbbox((0, 0), event_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    title_x = (canvas_width - title_width) // 2
    title_y = (padding_top - title_height) // 2
    draw.text((title_x, title_y), event_text, fill=(0, 0, 0), font=title_font)
    
    # Draw info text (quarter, clocks) in bottom padding area, with some margin
    info_x = int(canvas_width * 0.02)
    info_y = padding_top + background_img.height + 10
    draw.text((info_x, info_y), info_text, fill=(0, 0, 0), font=info_font)
    
    # Convert PIL Image to numpy array for imageio
    return np.array(canvas)


def animate_event(df, output_path, fps=10, figsize=(14, 8)):
    """Create MP4 animation of player movement using PIL for frame composition."""
    
    # timing = {}
    total_start = time.time()
    
    # step_start = time.time()

    if not validate_game(df):
        return

    # Create unique game_clock snapshots across all events, removing duplicates
    # timing['setup'] = time.time() - step_start
    # step_start = time.time()
    frames_data = dedupe_frames(df)
    # timing['frame_data_prep'] = time.time() - step_start
    
    # Create court background once and keep in memory
    # court_bg_start = time.time()
    print(f"Detecting coordinate mapping with test markers...")
    court_background, x_scale, y_scale, x_offset, y_offset = create_court_background_image(figsize=figsize)
    # timing['court_bg'] = time.time() - court_bg_start
    
    print(f"Rendering animation ({len(frames_data)} frames)...")
    # print(f"  Setup time: {timing['setup']:.3f}s")
    # print(f"  Frame data prep: {timing['frame_data_prep']:.3f}s")
    # print(f"  Court background + mapping detection: {timing['court_bg']:.3f}s")
    
    # scatter_total = 0
    # text_total = 0
    # compose_total = 0
    
    # Create MP4 from frames (write directly without temp files)
    print(f"\nEncoding MP4 to {output_path}...")
    encode_start = time.time()
    
    with imageio.get_writer(output_path, fps=fps, codec='libx264') as writer:
        for i, (applicable_events, game_clock, frame_df) in enumerate(frames_data):
            # Get all positions at this exact moment
            # scatter_start = time.time()
            positions_at_time = []
            colors_at_time = []
            sizes_at_time = []
            
            for _, data_row in frame_df.iterrows():
                positions_at_time.append([data_row['x_loc'], data_row['y_loc']])
                team = data_row['team_id']
                colors_at_time.append(TEAM_COLORS.get(team, 'gray'))
                sizes_at_time.append(300 if team == -1 else 200)
            # scatter_total += time.time() - scatter_start
            
            # Prepare text
            # text_start = time.time()
            first_row = frame_df.iloc[0]
            quarter = int(first_row['quarter'])
            shot_clock = first_row['shot_clock']
            
            # Format event IDs display
            if len(applicable_events) == 1:
                event_text = f'Event ID: {applicable_events[0]}'
            else:
                event_text = f'Event IDs: {", ".join(map(str, applicable_events))}'
            
            info_text = f'Quarter: {quarter}\nGame Clock: {game_clock:.2f}s\nShot Clock: {shot_clock:.2f}s'
            # text_total += time.time() - text_start
            
            # Compose frame with PIL using coordinate mapping
            # compose_start = time.time()
            frame_array = compose_frame_pil(court_background, positions_at_time, colors_at_time, 
                                            sizes_at_time, event_text, info_text, 
                                            x_scale, y_scale, x_offset, y_offset)
            # compose_total += time.time() - compose_start
            
            writer.append_data(frame_array)
            
            if (i + 1) % max(1, len(frames_data) // 20) == 0:
                print(f"  Rendered {i + 1}/{len(frames_data)} frames")
    
    encode_time = time.time() - encode_start
    print(f"  Encoding time: {encode_time:.3f}s")
    
    # print(f"\n--- Per-frame timing (totals across all {len(frames_data)} frames) ---")
    # print(f"  scatter:     {scatter_total:.3f}s ({scatter_total/len(frames_data):.3f}s/frame)")
    # print(f"  text:        {text_total:.3f}s ({text_total/len(frames_data):.3f}s/frame)")
    # print(f"  compose:     {compose_total:.3f}s ({compose_total/len(frames_data):.3f}s/frame)")
    
    total_time = time.time() - total_start
    print(f"\n✓ Animation saved: {output_path}")
    print(f"  {len(frames_data)} frames @ {fps} FPS = {len(frames_data)/fps:.1f}s video")
    print(f"  TOTAL TIME: {total_time:.3f}s")


def export_court_png(output_path='nba_court.png', figsize=(12, 8), dpi=150):
    """Export a clean NBA court diagram as PNG.
    
    Args:
        output_path: Path to save the PNG file
        figsize: Figure size as (width, height) in inches
        dpi: Resolution in dots per inch
    """
    fig, ax = plt.subplots(figsize=figsize)
    draw_court(ax)
    
    # Remove axis labels for cleaner diagram
    ax.set_title('NBA Basketball Court - Official Specifications', 
                 fontsize=16, weight='bold', pad=20)
    
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"✓ Court diagram saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Animate NBA player movement data')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Animate subcommand
    animate_parser = subparsers.add_parser('animate', help='Create animation from movement data')
    animate_parser.add_argument('csv', type=str, help='Path to movement CSV file')
    animate_parser.add_argument('--event-ids', type=int, nargs='+', default=[1, 1],
                               help='Event ID range (e.g., --event-ids 1 10) or list (e.g., --event-ids 1 5 7)')
    animate_parser.add_argument('--output', type=str, default='data/animations/animation.mp4',
                               help='Output MP4 file path')
    animate_parser.add_argument('--fps', type=int, default=25,
                               help='Frames per second for animation')
    animate_parser.add_argument('--figsize', type=float, nargs=2, default=[14, 8],
                               help='Figure size in inches (width height)')
    
    # Court subcommand
    court_parser = subparsers.add_parser('court', help='Export court diagram as PNG')
    court_parser.add_argument('--output', type=str, default='data/animations/nba_court.png',
                             help='Output PNG file path')
    court_parser.add_argument('--figsize', type=int, nargs=2, default=[12, 8],
                             help='Figure size (width height)')
    
    args = parser.parse_args()
    
    # Handle court export (no CSV needed)
    if args.command == 'court':
        export_court_png(output_path=args.output, figsize=tuple(args.figsize))
        return
    
    # Handle animation (requires CSV)
    if args.command != 'animate':
        parser.print_help()
        return
    
    # Validate input file
    if not Path(args.csv).exists():
        print(f"Error: CSV file '{args.csv}' not found")
        return
    
    # Load data
    print(f"Loading data from {args.csv}...")
    df = load_event_data(args.csv, args.event_ids)
    
    if df.empty:
        print(f"No data found for event IDs {args.event_ids}")
        return
    
    print(f"Loaded {len(df)} rows across {df['event_id'].nunique()} event(s)")
    
    # Create animation
    animate_event(df, args.output, fps=args.fps, figsize=tuple(args.figsize))


if __name__ == '__main__':
    main()
