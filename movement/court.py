#!/usr/bin/env python3
"""NBA court drawing utilities."""

import matplotlib.patches as patches
import numpy as np


# NBA court dimensions (in feet)
COURT_LENGTH = 94
COURT_WIDTH = 50


def _draw_court_skeleton(ax):
    """Draw the outer boundary, baselines, sidelines, and half court line."""
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


def _draw_center_circle(ax):
    """Draw the center court circle (6 ft outer, 2 ft inner)."""
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


def _draw_ft_lane_and_line(ax):
    """Draw free throw lanes and lines (both ends)."""
    center_y = COURT_WIDTH / 2
    
    for x_end in [0, COURT_LENGTH]:
        if x_end == 0:
            lane_x = 0
            ft_x = 19
        else:
            lane_x = COURT_LENGTH - 19
            ft_x = COURT_LENGTH - 19
        
        # Free throw lane rectangle: 16 ft wide × 19 ft deep
        lane_rect = patches.Rectangle((lane_x, center_y - 8), 19, 16,
                                      linewidth=2, edgecolor='black', facecolor='none')
        ax.add_patch(lane_rect)
        
        # Free throw line: solid line at x=19 (or x=75 for right)
        ax.plot([ft_x, ft_x], [center_y - 6, center_y + 6], 'k-', linewidth=2.5)


def _draw_basket_and_rim(ax):
    """Draw backboards and rims (both ends)."""
    center_y = COURT_WIDTH / 2
    
    for x_end in [0, COURT_LENGTH]:
        if x_end == 0:
            backboard_x = 4
            rim_x = 5.25
        else:
            backboard_x = COURT_LENGTH - 4
            rim_x = COURT_LENGTH - 5.25
        
        # Backboard: 6 feet wide rectangle at backboard position
        backboard_rect = patches.Rectangle((backboard_x - 0.15, center_y - 3), 0.3, 6,
                                          linewidth=3, edgecolor='black', facecolor='none')
        ax.add_patch(backboard_rect)
        
        # Rim: 18" inside diameter (0.75 ft radius)
        rim_circle = patches.Circle((rim_x, center_y), 0.75,
                                   linewidth=2, edgecolor='red', facecolor='none')
        ax.add_patch(rim_circle)


def _draw_ft_circle(ax):
    """Draw free throw circles (dashed inside paint, solid outside)."""
    center_y = COURT_WIDTH / 2
    
    for x_end in [0, COURT_LENGTH]:
        ft_x = 19 if x_end == 0 else COURT_LENGTH - 19
        
        if x_end == 0:
            # Left basket: inside part (x < 19) is dashed
            theta_inside = np.linspace(np.pi/2, 3*np.pi/2, 100)
            x_inside = ft_x + 6 * np.cos(theta_inside)
            y_inside = center_y + 6 * np.sin(theta_inside)
            ax.plot(x_inside, y_inside, 'k--', linewidth=2)
            
            # Outside part (x >= 19) is solid
            theta_outside = np.linspace(-np.pi/2, np.pi/2, 100)
            x_outside = ft_x + 6 * np.cos(theta_outside)
            y_outside = center_y + 6 * np.sin(theta_outside)
            ax.plot(x_outside, y_outside, 'k-', linewidth=2)
        else:
            # Right basket: inside part (x > 75) is dashed
            theta_inside = np.linspace(-np.pi/2, np.pi/2, 100)
            x_inside = ft_x + 6 * np.cos(theta_inside)
            y_inside = center_y + 6 * np.sin(theta_inside)
            ax.plot(x_inside, y_inside, 'k--', linewidth=2)
            
            # Outside part (x <= 75) is solid
            theta_outside = np.linspace(np.pi/2, 3*np.pi/2, 100)
            x_outside = ft_x + 6 * np.cos(theta_outside)
            y_outside = center_y + 6 * np.sin(theta_outside)
            ax.plot(x_outside, y_outside, 'k-', linewidth=2)


def _draw_restricted_area(ax):
    """Draw restricted area/charge circles (4 ft radius semicircle at baseline)."""
    center_y = COURT_WIDTH / 2
    
    for x_end in [0, COURT_LENGTH]:
        rim_x = 5.25 if x_end == 0 else COURT_LENGTH - 5.25
        
        if x_end == 0:
            restricted_theta = np.linspace(-np.pi/2, np.pi/2, 50)
        else:
            restricted_theta = np.linspace(np.pi/2, 3*np.pi/2, 50)
        
        restricted_x = rim_x + 4 * np.cos(restricted_theta)
        restricted_y = center_y + 4 * np.sin(restricted_theta)
        ax.plot(restricted_x, restricted_y, 'k-', linewidth=1.5)


def _draw_three_point_lines(ax):
    """Draw three-point lines (both ends)."""
    for x_end in [0, COURT_LENGTH]:
        if x_end == 0:
            # Left baseline
            rim_x = 5.25
            # Straight baseline sections (corners)
            ax.plot([0, 0], [0, 3], 'k-', linewidth=1.5)
            ax.plot([0, 0], [47, 50], 'k-', linewidth=1.5)
            
            # Parallel lines 3' from sideline
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
            
            ax.plot([79.8, COURT_LENGTH], [3, 3], 'k-', linewidth=1.5)
            ax.plot([79.8, COURT_LENGTH], [47, 47], 'k-', linewidth=1.5)
            
            # Arc: radius 23.75 ft centered at rim (88.75, 25), curving into court
            theta = np.linspace(np.pi - np.arcsin(22/23.75), np.pi + np.arcsin(22/23.75), 100)
            x_vals = rim_x + 23.75 * np.cos(theta)
            y_vals = 25 + 23.75 * np.sin(theta)
            ax.plot(x_vals, y_vals, 'k-', linewidth=1.5)


def _draw_calibration_markers(ax):
    """Draw calibration markers at court corners for coordinate mapping."""
    # Markers at the exact court corners: (0,0), (94,0), (0,50), (94,50)
    # Using magenta, green, blue, yellow to avoid visual interference
    ax.plot([0], [0], 'o', color=(1, 0, 1), markersize=10, markeredgecolor='black', markeredgewidth=1)
    ax.plot([COURT_LENGTH], [0], 'o', color=(0, 1, 0), markersize=10, markeredgecolor='black', markeredgewidth=1)
    ax.plot([0], [COURT_WIDTH], 'o', color=(0, 0, 1), markersize=10, markeredgecolor='black', markeredgewidth=1)
    ax.plot([COURT_LENGTH], [COURT_WIDTH], 'o', color=(1, 1, 0), markersize=10, markeredgecolor='black', markeredgewidth=1)


def draw_court(ax, markers=True):
    """Draw a complete NBA court with all elements.
    
    This is an orchestrator function that calls helper functions to draw:
    - Court skeleton (boundary, sidelines, half court line)
    - Center circle
    - Free throw lanes and lines
    - Baskets and rims
    - Free throw circles
    - Restricted areas
    - Three-point lines
    - Calibration markers for coordinate mapping
    
    Args:
        ax: matplotlib axes
    """
    _draw_court_skeleton(ax)
    _draw_center_circle(ax)
    _draw_ft_lane_and_line(ax)
    _draw_basket_and_rim(ax)
    _draw_ft_circle(ax)
    _draw_restricted_area(ax)
    _draw_three_point_lines(ax)
    if markers:
        _draw_calibration_markers(ax)
    
    # Set axes limits and aspect ratio
    ax.set_xlim(-3, COURT_LENGTH + 3)
    ax.set_ylim(-3, COURT_WIDTH + 3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.invert_yaxis()
