# NBA Basketball Court Specifications

## Overall Court Dimensions

| Dimension | Measurement | Notes |
|-----------|-------------|-------|
| **Length (Inside)** | 94 feet | From baseline to baseline |
| **Width (Inside)** | 50 feet | From sideline to sideline |
| **Total Area (Inside)** | 4,700 square feet | Playing surface only |
| **Minimum Apron Space** | 8 feet from baseline | Required surrounding space |
| **Minimum Total Space** | 110 feet (recommended) | From wall to wall |

---

## Court Markings & Features

### Baselines & Sidelines

| Element | Measurement | Notes |
|---------|-------------|-------|
| **Baseline** | 50 feet wide | End lines of the court |
| **Sideline** | 94 feet long | Side boundary lines |
| **Line Width** | 2 inches wide | All lines are 2 inches wide (neutral zones excluded) |

### Center Court

| Element | Measurement | Notes |
|---------|-------------|-------|
| **Center Court Line** | Divides court in half | Runs the full width of the court |
| **Center Circle (Inside)** | 2 ft radius (4 ft diameter) | Inner circle |
| **Center Circle (Outside)** | 6 ft radius (12 ft diameter) | Outer circle boundary |
| **Midcourt Location** | 47 feet from each baseline | Exact center of court |

### Free Throw Lane (The Paint)

| Element | Measurement | Notes |
|---------|-------------|-------|
| **Lane Width** | 16 feet | Full width of the rectangular lane |
| **Lane Depth** | 19 feet | From baseline to free throw line |
| **Lane Position (Left)** | x: 0 to 19, y: 17 to 33 | Rectangle with boundary lines |
| **Lane Position (Right)** | x: 75 to 94, y: 17 to 33 | Mirror of left side |
| **Boundary Lines** | Part of the lane | 2pt solid black |
| **Lane Space Marks** | 2 inches wide × 6 inches deep | NOT part of lane boundary |
| **Neutral Zone Marks** | Various | NOT part of lane boundary |

### Free Throw Line

| Element | Measurement | Notes |
|---------|-------------|-------|
| **Line Width** | 2 inches | Solid painted line |
| **Position** | 15 feet from backboard face | x = 19 (left), x = 75 (right) |
| **Line Length** | Crosses free throw circle | Runs parallel to end line |
| **Style** | Solid black, 2.5pt width | Not dashed |

### Free Throw Circle (The Arc at End of Lane)

| Element | Measurement | Notes |
|---------|-------------|-------|
| **Radius** | 6 feet | From free throw line center |
| **Circle Center** | (19, 25) left or (75, 25) right | At the free throw line |
| **Inside Paint** | Dashed line | Semicircle portion inside the lane |
| **Outside Paint** | Solid line | Semicircle portion outside the lane |
| **Line Style (Inside)** | 2pt dashed black | Distinguishes restricted shooting area |
| **Line Style (Outside)** | 2pt solid black | Main arc boundary |
| **Diameter** | 12 feet | Full circle extends 6 ft on each side of line |

### The Basket, Backboard & Rim

| Element | Measurement | Notes |
|---------|-------------|-------|
| **Rim Center Distance from Baseline** | 5 feet 3 inches | 5.25 feet exactly |
| **Backboard Distance from Baseline** | 4 feet | Backboard face position |
| **Backboard Width** | 6 feet | Horizontal dimension |
| **Backboard Height** | Approximately 3.5 feet | Vertical dimension (typical) |
| **Backboard Position (Left)** | x = 4, y: 22 to 28 | Rectangle centered at (4, 25) |
| **Backboard Position (Right)** | x = 90, y: 22 to 28 | Mirror of left side |
| **Backboard Line Style** | 3pt solid black | Thicker outline than court lines |
| **Rim Type** | NBA approved metal safety ring | Official equipment |
| **Rim Inside Diameter** | 18 inches | 0.75 feet radius |
| **Rim Position from Backboard** | 6 inches | 0.5 feet away from backboard face |
| **Rim Center (Left)** | (5.25, 25) | 1.25 feet in front of backboard |
| **Rim Center (Right)** | (88.75, 25) | 1.25 feet in front of backboard |
| **Rim Line Style** | 2pt solid red | Distinguishes from court markings |
| **Basket Height** | 10 feet | Measured from floor (not in 2D diagram) |

### Three-Point Line

| Element | Measurement | Notes |
|---------|-------------|-------|
| **Distance from Basket (Corners)** | 22 feet | Shortest distance to the line |
| **Distance from Basket (Top of Arc)** | 23 feet 9 inches | Furthest distance from basket |
| **Distance from Basket (Average)** | ~23.75 feet | Measured at various points along arc |
| **Sideline to Three-Point Line** | 14 feet | From sideline to edge of three-point arc |
| **Arc Radius** | Varies (22-23.75 ft) | Non-uniform arc creating a specific curve |
| **Three-Point Arc Measurement** | 20 feet 11 inches (outside) | Total distance from baseline to line center |

### Restricted Area (The Charge Circle)

| Element | Measurement | Notes |
|---------|-------------|-------|
| **Radius** | 4 feet (outside) | Semicircular arc at the baseline |
| **Arc Depth** | 4 feet from baseline | How far the arc extends into the court |
| **Purpose** | Defines defensive 3-second violation zone | No defensive player allowed here for more than 3 seconds without defensive action |

### Half-Court Line & Circle

| Element | Measurement | Notes |
|---------|-------------|-------|
| **Half-Court Line** | Runs full width (50 feet) | Divides home and away court |
| **Half-Court Circle (Inside)** | 2 ft radius | At center of court on each half |
| **Half-Court Circle (Outside)** | 6 ft radius | Outer boundary circle at midcourt |
| **Jump Circle Center** | 47 feet from each baseline | Exact midcourt location |

---

## Coordinate System Reference

When analyzing NBA movement data, coordinates are typically represented as (inside the playing court):

- **X-axis**: 0 to 94 feet (from one baseline to the other)
- **Y-axis**: 0 to 50 feet (from sideline to sideline)
- **Origin**: Usually placed at one baseline corner (0, 0) or at center court (47, 25)
- **Court Half**: X = 0-47 feet (offensive half) or X = 47-94 feet (defensive half)

---

## Key Distances for Play Analysis

| Scenario | Distance | Notes |
|----------|----------|-------|
| **Paint/Restricted Area** | 4 feet radius | Closest distance to basket |
| **Close Range Shot** | 0-10 feet | Layup/dunk zone inside the paint |
| **Inside Free Throw Lane** | 16 feet width | Direct lane under basket |
| **Outside Free Throw Lane** | 19 feet width | At the free throw line |
| **Mid-Range Shot** | 10-22 feet | Between lane and three-point line |
| **Three-Point Range (Corners)** | 22 feet | Shortest three-point distance |
| **Three-Point Range (Top)** | 23 feet 9 inches | Furthest three-point distance |
| **Half-Court Distance** | 47 feet | From one baseline to midcourt |
| **Full Court Distance** | 94 feet | Entire length of court |

---

## Additional Court Features

- **Court Surface**: Hardwood (typically maple)
- **Court Color**: Usually tan or light wood with dark lines
- **Team Logos**: Displayed at center court and corners
- **Advertising Boards**: Around the perimeter at 34 inches high
- **Shot Clock Displays**: 24 seconds (2023 update) / 14 seconds (offensive rebound)

---

## Image Specifications

This document is based on official NBA court dimension diagrams showing precise measurements:

- **Court Inside Dimensions**: 94 feet long × 50 feet wide
- **Minimum Surrounding Space**: 8 feet from baseline
- **Recommended Total Facility**: 110 feet minimum (wall to wall)
- **All Line Widths**: 2 inches (neutral zones excluded)
- **All Measurements**: From inside court lines

---

## Historical Context

As of the 2024 NBA season, the official court dimensions specified in this document remain unchanged from the established specifications. These measurements are consistent with:

- NBA Official Rules (Rule 1: The Court)
- FIBA (International Basketball Federation) standards for professional courts
- ABA (American Basketball Association) court specifications

The three-point line distance (22-23.75 feet) has been standardized since the 1997-98 season and is one of the most critical measurements for modern basketball analytics.

---

## How to Programmatically Build the NBA Court

This section provides detailed instructions for drawing each court element using standard graphics libraries (e.g., Matplotlib in Python).

### Coordinate System for Programming

- **Origin**: (0, 0) at baseline-left corner
- **X-axis**: 0 to 94 feet (left baseline to right baseline)
- **Y-axis**: 0 to 50 feet (bottom sideline to top sideline)
- **Center**: (47, 25)
- **Left basket (rim)**: (5.25, 25)
- **Right basket (rim)**: (88.75, 25)
- **Left backboard**: x = 4
- **Right backboard**: x = 90

### Element-by-Element Instructions

#### 1. Court Boundary (Perimeter)

Draw four lines forming the rectangle:

```
Line 1 (Left baseline):   from (0, 0) to (0, 50)
Line 2 (Right baseline):  from (94, 0) to (94, 50)
Line 3 (Bottom sideline): from (0, 0) to (94, 0)
Line 4 (Top sideline):    from (0, 50) to (94, 50)
```

**Style**: 2.5pt solid black

---

#### 2. Half-Court Line

Single vertical line at midcourt:

```
from (47, 0) to (47, 50)
```

**Style**: 2.5pt solid black

---

#### 3. Center Court Circles

Two concentric circles at (47, 25):

**Outer Circle:**
- Center: (47, 25)
- Radius: 6 feet
- Style: 2pt solid black, no fill

**Inner Circle:**
- Center: (47, 25)
- Radius: 2 feet
- Style: 2pt solid black, filled black

---

#### 4. Free Throw Lanes (The Paint)

Two rectangles, one at each end:

**Left lane:**
- Top-left corner: (0, 17)
- Bottom-right corner: (19, 33)
- Width: 16 feet (y: 17 to 33, centered at 25)
- Depth: 19 feet (x: 0 to 19, from baseline to free throw line)
- Style: 2pt solid black, no fill

**Right lane:**
- Top-left corner: (75, 17)
- Bottom-right corner: (94, 33)
- Width: 16 feet
- Depth: 19 feet
- Style: 2pt solid black, no fill

---

#### 5. Free Throw Line

Solid line across each free throw circle:

**Left side:**
- From: (19, 19)
- To: (19, 31)
- Width: 2.5pt solid black line
- Note: Positioned 15 feet from backboard face at (4, 25)

**Right side:**
- From: (75, 19)
- To: (75, 31)
- Width: 2.5pt solid black line
- Note: Positioned 15 feet from backboard face at (90, 25)

---

#### 6. Free Throw Circles (Split Solid/Dashed)

Semicircular arcs at the end of each lane, with different line styles on each side of the free throw line:

**Left arc (centered at (19, 25) with 6 ft radius):**

Inside Paint (Dashed):
- The semicircle facing the baseline (x < 19)
- Formula: x = 19 + 6*cos(θ), y = 25 + 6*sin(θ)
- θ ranges from π/2 to 3π/2 (180 degrees)
- Style: 2pt dashed black

Outside Paint (Solid):
- The semicircle facing away from baseline (x > 19)
- Formula: x = 19 + 6*cos(θ), y = 25 + 6*sin(θ)
- θ ranges from -π/2 to π/2 (180 degrees)
- Style: 2pt solid black

**Right arc (centered at (75, 25) with 6 ft radius):**

Inside Paint (Dashed):
- The semicircle facing the baseline (x > 75)
- Formula: x = 75 + 6*cos(θ), y = 25 + 6*sin(θ)
- θ ranges from -π/2 to π/2
- Style: 2pt dashed black

Outside Paint (Solid):
- The semicircle facing away from baseline (x < 75)
- Formula: x = 75 + 6*cos(θ), y = 25 + 6*sin(θ)
- θ ranges from π/2 to 3π/2
- Style: 2pt solid black

---

#### 6. Restricted Area (Charge Circle)

Semicircular arc near baseline at each basket:

**Left restricted area:**
- Center: (4, 25)
- Radius: 4 feet
- Baseline segment: from (0, 21) to (0, 29) (straight line on baseline)
- Arc: semicircle from (0, 21) to (0, 29) extending into court
- Formula: x = 4 + 4*cos(θ), y = 25 + 4*sin(θ), θ from 0 to π
- Style: 1.5pt solid black

**Right restricted area:**
- Center: (90, 25)
- Radius: 4 feet
- Baseline segment: from (94, 21) to (94, 29)
- Formula: x = 90 + 4*cos(θ), y = 25 + 4*sin(θ), θ from π to 2π
- Style: 1.5pt solid black

---

#### 7. Three-Point Line - THE DETAILED BREAKDOWN

This is the most complex element. Official rule:

> "The three-point field goal area has parallel lines 3' from the sidelines, extending from the baseline for 14 feet, and an arc of 23'9" from the middle of the basket which intersects the parallel lines."

**Implementation:**

**Left side (x=0 baseline):**

1. **Baseline corners** (connect sideline to parallel line):
   ```
   Line 1: from (0, 0) to (0, 3)
   Line 2: from (0, 47) to (0, 50)
   ```

2. **Parallel lines** (3 feet from sidelines):
   - Geometric calculation for where the arc intersects:
   - Distance from basket (5.25, 25) to point at y=3 should equal 23.75 ft
   - sqrt((x-5.25)² + (3-25)²) = 23.75
   - (x-5.25)² + 484 = 564.0625
   - (x-5.25)² = 80.0625
   - x ≈ 14.2 feet
   
   ```
   Line 1: from (0, 3) to (14.2, 3)
   Line 2: from (0, 47) to (14.2, 47)
   ```

3. **Arc** (23.75 feet radius from basket):
   - Center: (5.25, 25)
   - Radius: 23.75 feet
   - Starting angle: θ = arcsin((3-25)/23.75) = arcsin(-22/23.75) ≈ -1.144 rad
   - Ending angle: θ = arcsin((47-25)/23.75) = arcsin(22/23.75) ≈ 1.144 rad
   - Formula: x = 5.25 + 23.75*cos(θ), y = 25 + 23.75*sin(θ)
   - Style: 1.5pt solid black

**Right side (x=94 baseline):**

1. **Baseline corners:**
   ```
   Line 1: from (94, 0) to (94, 3)
   Line 2: from (94, 47) to (94, 50)
   ```

2. **Parallel lines** (3 feet from sidelines):
   - Mirror calculation: x = 94 - 14.2 = 79.8 feet
   ```
   Line 1: from (79.8, 3) to (94, 3)
   Line 2: from (79.8, 47) to (94, 47)
   ```

3. **Arc** (23.75 feet radius from basket):
   - Center: (88.75, 25)
   - Starting angle: θ = π - arcsin(22/23.75) ≈ 4.287 rad
   - Ending angle: θ = π + arcsin(22/23.75) ≈ 4.287 rad
   - Formula: x = 88.75 + 23.75*cos(θ), y = 25 + 23.75*sin(θ)
   - Style: 1.5pt solid black

---

#### 8. Backboards

Two rectangular outlines representing the backboards:

**Left backboard:**
- Position: x = 4 feet from baseline
- Dimensions: 0.3 feet wide × 6 feet tall
- Coordinates: Rectangle from (3.85, 22) to (4.15, 28)
- Style: 3pt solid black (thicker than court lines)

**Right backboard:**
- Position: x = 90 feet from baseline
- Dimensions: 0.3 feet wide × 6 feet tall
- Coordinates: Rectangle from (89.85, 22) to (90.15, 28)
- Style: 3pt solid black

---

#### 9. Rim (Basket)

Two circles representing the 18-inch diameter basketball rims:

**Left rim:**
- Center: (5.25, 25)
- Inside Diameter: 18 inches = 0.75 feet radius
- Distance from backboard: 1.25 feet (5.25 - 4 = 1.25)
- Style: 2pt solid red circle

**Right rim:**
- Center: (88.75, 25)
- Inside Diameter: 18 inches = 0.75 feet radius
- Distance from backboard: 1.25 feet (90 - 88.75 = 1.25)
- Style: 2pt solid red circle

---

### Drawing Order (Recommended)

1. Court boundary (rectangle)
2. Court background fill (optional: light wood color)
3. Half-court line
4. Free throw lanes (both ends)
5. Free throw lines (both ends)
6. Free throw circles (both ends) - split solid/dashed
7. Restricted areas (both ends)
8. Three-point lines (both ends)
9. Center court circles (outer, then inner)
10. Backboards (both ends)
11. Rims (both ends)
7. Three-point lines (both ends)
8. Center court circles (outer, then inner)
9. Basket positions (red markers)
10. Backboards (both ends)

---

### Discrepancy Note: Official Rule vs. Geometric Reality

**The Three-Point Line's 14-Foot Baseline Measurement:**

The official NBA rule states that the parallel lines extend "for 14 feet" from the baseline. However, geometric calculation shows this creates a gap or overlap with the arc:

- **Official specification**: 14 feet
- **Calculated flush connection**: 12.95 feet
- **Difference**: ~1.05 feet (12.6 inches)

When drawing to match the official 23'9" arc precisely, the parallel lines should end at 12.95 feet for exact flush connection. Most modern court diagrams use this calculated value. This guide documents both values for reference.



- Official NBA.com Court Specifications & Diagrams
- NBA Official Rules and Regulations
- FIBA Rulebook (Rule 2: The Court)
- NBA Stats API coordinate system
- Professional basketball tracking data standards

