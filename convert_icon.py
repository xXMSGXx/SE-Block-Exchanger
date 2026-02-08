"""
Convert logo image to app_icon.ico and related files for the SE Block Exchanger.
Accepts logo.png, logo.jpeg, or logo.jpg as input.
Requires: pip install Pillow
Usage: python convert_icon.py
"""

from PIL import Image
import sys
import os

LOGO_CANDIDATES = ["logo.png", "logo.jpeg", "logo.jpg"]


def find_logo():
    """Find the first available logo file in the project root."""
    for name in LOGO_CANDIDATES:
        if os.path.exists(name):
            return name
    return None


def convert_logo_to_ico(input_path=None, output_path="app_icon.ico"):
    if input_path is None:
        input_path = find_logo()
    if input_path is None or not os.path.exists(input_path):
        print("Error: No logo file found.")
        print(f"Please save your logo as one of {LOGO_CANDIDATES} in the project root.")
        sys.exit(1)

    img = Image.open(input_path).convert("RGBA")
    print(f"Source: {input_path} — {img.size[0]}x{img.size[1]}")

    # Save logo.png (what the GUI header expects)
    img.save("logo.png", "PNG")
    print("Saved logo.png")

    # Save app_icon.png (fallback for GUI header)
    img.save("app_icon.png", "PNG")
    print("Saved app_icon.png")

    # Create multi-size .ico for window icon
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(output_path, format="ICO", sizes=sizes)
    print(f"Saved {output_path} with sizes: {sizes}")


if __name__ == "__main__":
    convert_logo_to_ico()
