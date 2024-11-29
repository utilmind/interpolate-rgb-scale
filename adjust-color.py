"""
Filename: adjust-color.py
Description: Adjust the brightness of an RGB color or a single channel.

    Args:
        color (tuple or int): RGB values of the color (e.g., (255, 255, 120)) or single channel.
        intensity_factor (float): Percentage to adjust brightness (e.g., -0.33 to darken by 33%).
    Returns:
        tuple or int: Adjusted RGB color or single channel value.

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

import argparse

def adjust_channel(value, intensity_factor):
    """
    Adjust a single channel value by a given intensity factor.
    Args:
        value (int): Value of the channel (0–255).
        intensity_factor (float): Percentage to adjust brightness (e.g., -0.33 to darken by 33%).
    Returns:
        int: Adjusted channel value.
    """
    return max(0, min(255, int(value * (1 + intensity_factor))))


def adjust_color(color, intensity_factor):
    """
    Adjust the brightness of an RGB color or a single channel.
    Args:
        color (tuple or int): RGB values of the color (e.g., (255, 255, 120)) or single channel.
        intensity_factor (float): Percentage to adjust brightness (e.g., -0.33 to darken by 33%).
    Returns:
        tuple or int: Adjusted RGB color or single channel value.
    """
    if isinstance(color, int):
        return adjust_channel(color, intensity_factor)
    return tuple(adjust_channel(channel, intensity_factor) for channel in color)


def parse_color(color_str):
    """
    Parse the input color string into a tuple or int.
    Args:
        color_str (str): Input color string (e.g., '255,255,120' or '100' or '0x64').
    Returns:
        tuple or int: Parsed color value.
    Raises:
        ValueError: If the color format is invalid.
    """
    if "," in color_str:  # RGB format
        color = tuple(map(int, color_str.split(",")))
        if len(color) != 3 or not all(0 <= c <= 255 for c in color):
            raise ValueError
    else:  # Single channel, support hex (0x..) and decimal
        color = int(color_str, 0)  # Automatically handles decimal and hex
        if not (0 <= color <= 255):
            raise ValueError
    return color


def format_color(value):
    """
    Format a color value as both decimal and hexadecimal.
    Args:
        value (int): Color value (0–255).
    Returns:
        str: Formatted string (e.g., '120 (0x78)').
    """
    return f"{value} (0x{value:02X})"


def main():
    parser = argparse.ArgumentParser(description="Adjust the brightness of an RGB color or a single channel.")
    parser.add_argument(
        "color",
        type=str,
        help="Input color: either 'R,G,B' (e.g., '255,255,120'), a single value (e.g., '100'), or a hex value (e.g., '0x64').",
    )
    parser.add_argument(
        "intensity",
        type=float,
        help="Intensity adjustment factor (e.g., -0.33 to darken by 33%, 0.2 to brighten by 20%).",
    )

    args = parser.parse_args()

    # Parse the input color
    try:
        color = parse_color(args.color)
    except ValueError:
        print("Error: Invalid color format. Use 'R,G,B', a single value between 0 and 255, or a hex value (e.g., '0x64').")
        return

    # Adjust the color
    adjusted_color = adjust_color(color, args.intensity)

    # Output the result
    if isinstance(color, int):
        print(f"Original channel: {format_color(color)}")
        print(f"Adjusted channel: {format_color(adjusted_color)}")
    else:
        original_color_formatted = ", ".join(format_color(c) for c in color)
        adjusted_color_formatted = ", ".join(format_color(c) for c in adjusted_color)
        print(f"Original color: rgb({original_color_formatted})")
        print(f"Adjusted color: rgb({adjusted_color_formatted})")


if __name__ == "__main__":
    main()
