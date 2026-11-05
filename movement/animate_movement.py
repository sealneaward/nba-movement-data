#!/usr/bin/env python3
"""
Animate NBA player movement data to MP4 video.
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.animation import FuncAnimation
import imageio.v2 as imageio
from pathlib import Path


# NBA court dimensions (in feet)
COURT_LENGTH = 94
COURT_WIDTH = 50


def draw_court(ax):
    """Draw an NBA court with official specifications."""
    # Outer boundary (court playing surface)
    ax.add_patch(patches.Rectangle((0, 0), COURT_LENGTH, COURT_WIDTH, 
                                    linewidth=2.5, edgecolor='black', facecolor='wheat', alpha=0.4))
    
    # Baselines (end lines)
    ax.plot([0, 0], [0, COURT_WIDTH], 'k-', linewidth=2.5)
    ax.plot([COURT_LENGTH, COURT_LENGTH], [0, COURT_WIDTH], 'k-', linewidth=2.5)
    
    # Sidelines
    ax.plot([0, COURT_LENGTH], [0, 0], 'k-', linewidth=2.5)
    ax.plot([0, COURT_LENGTH], [COURT_WIDTH, COURT_WIDTH], 'k-', linewidth=2.5)
    
    # Half court line (dividing line at midcourt)
    ax.plot([COURT_LENGTH/2, COURT_LENGTH/2], [0, COURT_WIDTH], 'k-', linewidth=2.5)
    
    # Center circle: outer (6 ft radius) and inner (2 ft radius)
    center_x = COURT_LENGTH / 2
    center_y = COURT_WIDTH / 2
    
    # Outer circle (6 ft radius)
    center_circle_outer = patches.Circle((center_x, center_y), 6, 
                                        linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(center_circle_outer)
    
    # Inner circle (2 ft radius)
    center_circle_inner = patches.Circle((center_x, center_y), 2, 
                                        linewidth=2, edgecolor='black', facecolor='black')
    ax.add_patch(center_circle_inner)
    
    # Free throw lane and baskets (both ends)
    for x_end in [0, COURT_LENGTH]:
        if x_end == 0:
            # Left end
            lane_x = 0
            ft_x = 19
            backboard_x = 4
            rim_x = 5.25
        else:
            # Right end
            lane_x = COURT_LENGTH - 19
            ft_x = COURT_LENGTH - 19
            backboard_x = COURT_LENGTH - 4
            rim_x = COURT_LENGTH - 5.25
        
        # Free throw lane rectangle: 16 ft wide × 19 ft deep
        # Lane depth: from baseline (x=0) to free throw line (x=19)
        # Lane width: 16 ft centered at y=25, so y = 17 to 33
        lane_rect = patches.Rectangle((lane_x, center_y - 8), 19, 16,
                                      linewidth=2, edgecolor='black', facecolor='none')
        ax.add_patch(lane_rect)
        
        # Free throw line: solid 2" wide line at x=19 (or x=75 for right)
        # Line extends across the full free throw circle (y from 19 to 31)
        ax.plot([ft_x, ft_x], [center_y - 6, center_y + 6], 'k-', linewidth=2.5)
        
        # Free throw circle (6 ft radius) - part inside paint is dashed, outside is solid
        if x_end == 0:
            # Left basket: paint is from x=0 to x=19, circle is centered at x=19
            # Inside part (x < 19): dashed
            theta_inside = np.linspace(np.pi/2, 3*np.pi/2, 100)
            x_inside = ft_x + 6 * np.cos(theta_inside)
            y_inside = center_y + 6 * np.sin(theta_inside)
            ax.plot(x_inside, y_inside, 'k--', linewidth=2)
            
            # Outside part (x >= 19): solid
            theta_outside = np.linspace(-np.pi/2, np.pi/2, 100)
            x_outside = ft_x + 6 * np.cos(theta_outside)
            y_outside = center_y + 6 * np.sin(theta_outside)
            ax.plot(x_outside, y_outside, 'k-', linewidth=2)
        else:
            # Right basket: paint is from x=75 to x=94, circle is centered at x=75
            # Inside part (x > 75): dashed
            theta_inside = np.linspace(-np.pi/2, np.pi/2, 100)
            x_inside = ft_x + 6 * np.cos(theta_inside)
            y_inside = center_y + 6 * np.sin(theta_inside)
            ax.plot(x_inside, y_inside, 'k--', linewidth=2)
            
            # Outside part (x <= 75): solid
            theta_outside = np.linspace(np.pi/2, 3*np.pi/2, 100)
            x_outside = ft_x + 6 * np.cos(theta_outside)
            y_outside = center_y + 6 * np.sin(theta_outside)
            ax.plot(x_outside, y_outside, 'k-', linewidth=2)
        
        # Restricted area/charge circle (4 ft radius semicircle at baseline)
        if x_end == 0:
            restricted_theta = np.linspace(-np.pi/2, np.pi/2, 50)
            restricted_x = rim_x + 4 * np.cos(restricted_theta)
            restricted_y = center_y + 4 * np.sin(restricted_theta)
        else:
            restricted_theta = np.linspace(np.pi/2, 3*np.pi/2, 50)
            restricted_x = rim_x + 4 * np.cos(restricted_theta)
            restricted_y = center_y + 4 * np.sin(restricted_theta)
        ax.plot(restricted_x, restricted_y, 'k-', linewidth=1.5)
        
        # Backboard: 6 feet wide rectangle at backboard position
        # Left: x=4, spans from y=22 to y=28 (6 feet tall, centered at y=25)
        # Right: x=90, spans from y=22 to y=28
        backboard_rect = patches.Rectangle((backboard_x - 0.15, center_y - 3), 0.3, 6,
                                          linewidth=3, edgecolor='black', facecolor='none')
        ax.add_patch(backboard_rect)
        
        # Rim: 18" inside diameter (0.75 ft radius), 6" from backboard face
        # Left: center at (5.75, 25), Right: center at (88.25, 25)
        rim_circle = patches.Circle((rim_x, center_y), 0.75,
                                   linewidth=2, edgecolor='red', facecolor='none')
        ax.add_patch(rim_circle)
    
    # Three-point lines (both ends)
    # Official rule: parallel lines 3' from sidelines extending from baseline,
    # and arc of 23'9" (23.75 ft) from basket center intersecting those parallel lines
    # Rim center is at 5.25 feet from baseline
    
    for x_end in [0, COURT_LENGTH]:
        if x_end == 0:
            # Left baseline
            rim_x = 5.25
            # Straight baseline sections (corners)
            ax.plot([0, 0], [0, 3], 'k-', linewidth=1.5)
            ax.plot([0, 0], [47, 50], 'k-', linewidth=1.5)
            
            # Parallel lines 3' from sideline, extending from baseline until arc
            # Distance from basket (5.25, 25) to parallel line at y=3 equals 23.75 ft
            # sqrt((x-5.25)² + (3-25)²) = 23.75
            # (x-5.25)² + 484 = 564.0625, so x ≈ 14.2
            ax.plot([0, 14.2], [3, 3], 'k-', linewidth=1.5)
            ax.plot([0, 14.2], [47, 47], 'k-', linewidth=1.5)
            
            # Arc: radius 23.75 ft centered at rim (5.25, 25), curving into court
            theta = np.linspace(-np.arcsin(22/23.75), np.arcsin(22/23.75), 100)
            x_vals = rim_x + 23.75 * np.cos(theta)
            y_vals = 25 + 23.75 * np.sin(theta)
            ax.plot(x_vals, y_vals, 'k-', linewidth=1.5)
        else:
            # Right baseline (mirror of left)
            rim_x = COURT_LENGTH - 5.25
            ax.plot([COURT_LENGTH, COURT_LENGTH], [0, 3], 'k-', linewidth=1.5)
            ax.plot([COURT_LENGTH, COURT_LENGTH], [47, 50], 'k-', linewidth=1.5)
            
            # x = 94 - 14.2 = 79.8
            ax.plot([79.8, COURT_LENGTH], [3, 3], 'k-', linewidth=1.5)
            ax.plot([79.8, COURT_LENGTH], [47, 47], 'k-', linewidth=1.5)
            
            # Arc: radius 23.75 ft centered at rim (88.75, 25), curving into court
            theta = np.linspace(np.pi - np.arcsin(22/23.75), np.pi + np.arcsin(22/23.75), 100)
            x_vals = rim_x + 23.75 * np.cos(theta)
            y_vals = 25 + 23.75 * np.sin(theta)
            ax.plot(x_vals, y_vals, 'k-', linewidth=1.5)
    
    ax.set_xlim(-3, COURT_LENGTH + 3)
    ax.set_ylim(-3, COURT_WIDTH + 3)
    ax.set_aspect('equal')
    ax.set_xlabel('Court Length (ft)', fontsize=11)
    ax.set_ylabel('Court Width (ft)', fontsize=11)
    ax.invert_yaxis()


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


def animate_event(df, output_path, fps=10, figsize=(14, 8)):
    """Create MP4 animation of player movement."""
    
    events = sorted(df['event_id'].unique())
    
    if len(events) == 0:
        print("No events found in the filtered data.")
        return
    
    # Color mapping for teams
    team_colors = {
        1610612761: '#1f77b4',  # Blue
        1610612766: '#ff7f0e',  # Orange
        -1: 'black'  # Ball
    }
    
    # Get unique teams and assign colors
    unique_teams = df['team_id'].unique()
    team_list = [t for t in unique_teams if t != -1]
    if len(team_list) >= 2:
        team_colors[team_list[0]] = '#1f77b4'
        team_colors[team_list[1]] = '#ff7f0e'
    
    # Create unique game_clock snapshots within each event
    frames_data = []
    for event_id in events:
        event_df = df[df['event_id'] == event_id]
        # Get unique timestamps and sort in descending order (game_clock counts down)
        unique_times = sorted(event_df['game_clock'].unique(), reverse=True)
        for game_clock in unique_times:
            # Get ALL rows at this exact timestamp
            frame_data = event_df[event_df['game_clock'] == game_clock]
            frames_data.append((event_id, game_clock, frame_data))
    
    print(f"Rendering animation ({len(frames_data)} frames)...")
    temp_frames = []
    
    for i, (event_id, game_clock, frame_df) in enumerate(frames_data):
        fig, ax = plt.subplots(figsize=figsize)
        draw_court(ax)
        
        # Get all positions at this exact moment
        positions_at_time = []
        colors_at_time = []
        sizes_at_time = []
        
        for _, data_row in frame_df.iterrows():
            positions_at_time.append([data_row['x_loc'], data_row['y_loc']])
            team = data_row['team_id']
            colors_at_time.append(team_colors.get(team, 'gray'))
            sizes_at_time.append(300 if team == -1 else 200)
        
        if positions_at_time:
            positions_array = np.array(positions_at_time)
            ax.scatter(positions_array[:, 0], positions_array[:, 1], 
                      s=sizes_at_time, c=colors_at_time, alpha=0.7, 
                      edgecolors='black', linewidth=1.5)
        
        # Add info text - use first row for quarter/shot_clock
        first_row = frame_df.iloc[0]
        quarter = int(first_row['quarter'])
        shot_clock = first_row['shot_clock']
        
        ax.text(0.5, 1.02, f'Event ID: {event_id}', transform=ax.transAxes,
               ha='center', fontsize=14, weight='bold')
        ax.text(0.02, 0.98, f'Quarter: {quarter}\nGame Clock: {game_clock:.2f}s\nShot Clock: {shot_clock:.2f}s',
               transform=ax.transAxes, va='top', fontsize=10, family='monospace')
        
        temp_file = f'/tmp/frame_{i:06d}.png'
        fig.savefig(temp_file, dpi=100, bbox_inches='tight')
        temp_frames.append(temp_file)
        plt.close(fig)
        
        if (i + 1) % max(1, len(frames_data) // 20) == 0:
            print(f"  Rendered {i + 1}/{len(frames_data)} frames")
    
    # Create MP4 from frames
    print(f"Encoding MP4 to {output_path}...")
    with imageio.get_writer(output_path, fps=fps, codec='libx264') as writer:
        for frame_file in temp_frames:
            image = imageio.imread(frame_file)
            writer.append_data(image)
    
    # Clean up temp files
    import os
    for frame_file in temp_frames:
        if os.path.exists(frame_file):
            os.remove(frame_file)
    
    print(f"✓ Animation saved: {output_path}")
    print(f"  {len(temp_frames)} frames @ {fps} FPS = {len(temp_frames)/fps:.1f}s video")


def export_court_png(output_path='nba_court.png', figsize=(14, 8), dpi=150):
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
    animate_parser.add_argument('--figsize', type=int, nargs=2, default=[14, 8],
                               help='Figure size (width height)')
    
    # Court subcommand
    court_parser = subparsers.add_parser('court', help='Export court diagram as PNG')
    court_parser.add_argument('--output', type=str, default='data/animations/nba_court.png',
                             help='Output PNG file path')
    court_parser.add_argument('--figsize', type=int, nargs=2, default=[14, 8],
                             help='Figure size (width height)')
    court_parser.add_argument('--dpi', type=int, default=150,
                             help='Resolution in dots per inch')
    
    args = parser.parse_args()
    
    # Handle court export (no CSV needed)
    if args.command == 'court':
        export_court_png(output_path=args.output, figsize=tuple(args.figsize), dpi=args.dpi)
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
