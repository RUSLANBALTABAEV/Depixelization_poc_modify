import os
import argparse
from typing import cast, Tuple


def check_file(s: str) -> str:
    """Check if file exists."""
    if os.path.isfile(s):
        return s
    else:
        raise argparse.ArgumentTypeError(f"{s!r} is not a file.")


def check_color(s: str | None) -> Tuple[int, int, int] | None:
    """Parse color string in format 'r,g,b'."""
    if s is None:
        return None
    ss = s.split(",")
    if len(ss) != 3:
        raise argparse.ArgumentTypeError("Given colors must be formatted as 'r,g,b'.")
    else:
        try:
            rgb = tuple([int(i.strip()) for i in ss])
            # Validate range
            for val in rgb:
                if not 0 <= val <= 255:
                    raise ValueError(f"RGB value {val} out of range 0-255")
            return cast(Tuple[int, int, int], rgb)
        except ValueError as e:
            raise argparse.ArgumentTypeError(
                f"Invalid color format {s!r}: {str(e)}"
            )


def rgb_to_hex(color: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex string."""
    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError(f"Invalid hex color: {hex_color}")


def calculate_color_distance(
    color1: Tuple[int, int, int],
    color2: Tuple[int, int, int]
) -> float:
    """Calculate Euclidean distance between two colors."""
    return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5


def are_colors_similar(
    color1: Tuple[int, int, int],
    color2: Tuple[int, int, int],
    threshold: float = 10.0
) -> bool:
    """Check if two colors are similar within threshold."""
    return calculate_color_distance(color1, color2) <= threshold
