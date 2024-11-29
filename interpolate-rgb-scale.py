"""
Filename: interpolate-rgb-scale.py
Description: A script to interpolate colors on a scale between predefined points.
Just fill the colors of key points and it will fill the missing points of scale.

Author: https://github.com/utilmind/
Date Created: 2024-11-28
Last Modified: 2024-11-28
Version: 1.0
License: MIT License

Dependencies:
- Python 3.6 or higher
- No external libraries

Usage:
Run this script directly to see interpolated colors for a predefined scale.
"""

def interpolate_color(start_color, end_color, start_pos, end_pos, pos):
    """
    Linearly interpolate the color between two given colors.

    Args:
        start_color (tuple): RGB values of the starting color.
        end_color (tuple): RGB values of the ending color.
        start_pos (int): Starting position on the scale.
        end_pos (int): Ending position on the scale.
        pos (int): The position for which we need to find the interpolated color.

    Returns:
        tuple: Interpolated RGB color at the given position.
    """
    return tuple(
        int(start + (end - start) * (pos - start_pos) / (end_pos - start_pos))
        for start, end in zip(start_color, end_color)
    )


def darken_color(color, reduction_factor=0.33):
    """
    Darken the given RGB color by reducing each channel by a percentage.
    (So if channel color is FF, brightness will be reduced to AA, if reduction_factor is 0.33 (33%).)

    Args:
        color (tuple): RGB values of the color (e.g., (255, 255, 120)).
        reduction_factor (float): Percentage to reduce each channel (e.g., 0.33 for 33%).

    Returns:
        tuple: Darkened RGB color.
    """
    return tuple(int(channel * (1 - reduction_factor)) for channel in color)


# Define key points on the scale with their corresponding colors
"""
colors = {
    1: (0, 255, 0),     # Green
    3: (255, 255, 0),   # Yellow
    5: (255, 165, 0),   # Orange
    7: (255, 0, 0),     # Red
}
"""
colors = {
    # Alternative, soft colors from https://wio-dev.avmet.com/
    1: (176, 238, 176),   # Soft Green
    3: (255, 255, 120),   # Soft Yellow
    7: (248, 152, 150),   # Soft Red
    9: (124,  76,  75),   # Dark Red
}

# Calculate the orange color (average of yellow and red)
yellow = colors[3]
red = colors[7]
colors[5] = tuple((yellow[i] + red[i]) // 2 for i in range(3))  # Soft Orange

# Generate colors for all points on the scale (from 1 to 9)
scale_points = range(1, 10)
result = []  # List to store the results

for i in scale_points:
    if i in colors:
        # If the point has a predefined color, use it directly
        bg_color = colors[i]
    else:
        # Find the nearest lower and upper bounds for interpolation
        lower_bound = max(k for k in colors if k < i)
        upper_bound = min(k for k in colors if k > i)
        # Interpolate the color for the current point
        bg_color = interpolate_color(
            colors[lower_bound], colors[upper_bound], lower_bound, upper_bound, i
        )
    # Calculate border color by darkening the background color
    border_color = darken_color(bg_color)
    result.append((i, bg_color, border_color))

# Print the results
for point, bg_color, border_color in result:
    bg_color_str = ' '.join(map(str, bg_color))  # convert (176, 238, 176) -> "176 238 176", strip commas.
    border_color_str = ' '.join(map(str, border_color))  # the same as above
    print(f".airport.i{point} {{ background-color: rgb({bg_color_str}); border-color: rgb({border_color_str}); }}")
