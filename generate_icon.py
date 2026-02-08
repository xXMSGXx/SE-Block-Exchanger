"""
Generate a Meraby Labs branded icon for SE Block Exchanger.
Creates app_icon.ico with the tactical hologram color scheme.
"""

from PIL import Image, ImageDraw, ImageFont
import os


def generate_icon():
    """Create a Meraby Labs branded icon matching the tactical hologram theme."""
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background: rounded-ish dark gunmetal square
    bg_color = (15, 23, 42, 255)       # #0f172a  BG_DARK
    cyan = (6, 182, 212, 255)          # #06b6d4  CYAN_PRIMARY
    orange = (245, 158, 11, 255)       # #f59e0b  ORANGE_PRIMARY
    text_cyan = (103, 232, 249, 255)   # #67e8f9  TEXT_CYAN

    # Draw filled background
    draw.rounded_rectangle([4, 4, size - 5, size - 5], radius=32, fill=bg_color)

    # Outer border — cyan
    draw.rounded_rectangle([4, 4, size - 5, size - 5], radius=32, outline=cyan, width=4)

    # Inner accent border — orange
    draw.rounded_rectangle([14, 14, size - 15, size - 15], radius=24, outline=orange, width=2)

    # Corner brackets (tactical targeting aesthetic)
    blen = 30
    bw = 3
    # Top-left
    draw.line([(24, 24), (24 + blen, 24)], fill=cyan, width=bw)
    draw.line([(24, 24), (24, 24 + blen)], fill=cyan, width=bw)
    # Top-right
    draw.line([(size - 25, 24), (size - 25 - blen, 24)], fill=cyan, width=bw)
    draw.line([(size - 25, 24), (size - 25, 24 + blen)], fill=cyan, width=bw)
    # Bottom-left
    draw.line([(24, size - 25), (24 + blen, size - 25)], fill=cyan, width=bw)
    draw.line([(24, size - 25), (24, size - 25 - blen)], fill=cyan, width=bw)
    # Bottom-right
    draw.line([(size - 25, size - 25), (size - 25 - blen, size - 25)], fill=cyan, width=bw)
    draw.line([(size - 25, size - 25), (size - 25, size - 25 - blen)], fill=cyan, width=bw)

    # Draw "SE" large centered text
    try:
        font_large = ImageFont.truetype("courbd.ttf", 88)
    except OSError:
        try:
            font_large = ImageFont.truetype("cour.ttf", 88)
        except OSError:
            font_large = ImageFont.load_default()

    # "SE" in orange
    bbox = draw.textbbox((0, 0), "SE", font=font_large)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size - tw) // 2
    ty = (size - th) // 2 - 24
    draw.text((tx, ty), "SE", fill=orange, font=font_large)

    # Draw "BCX" smaller below
    try:
        font_small = ImageFont.truetype("courbd.ttf", 36)
    except OSError:
        try:
            font_small = ImageFont.truetype("cour.ttf", 36)
        except OSError:
            font_small = ImageFont.load_default()

    bbox2 = draw.textbbox((0, 0), "BCX", font=font_small)
    tw2 = bbox2[2] - bbox2[0]
    tx2 = (size - tw2) // 2
    ty2 = ty + th + 8
    draw.text((tx2, ty2), "BCX", fill=text_cyan, font=font_small)

    # "MERABY LABS" tiny at bottom
    try:
        font_tiny = ImageFont.truetype("cour.ttf", 16)
    except OSError:
        font_tiny = ImageFont.load_default()

    bbox3 = draw.textbbox((0, 0), "MERABY LABS", font=font_tiny)
    tw3 = bbox3[2] - bbox3[0]
    draw.text(((size - tw3) // 2, size - 42), "MERABY LABS", fill=cyan, font=font_tiny)

    # Save as multi-size ICO
    icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_icon.ico')
    img.save(icon_path, format='ICO', sizes=icon_sizes)
    print(f"Icon saved to: {icon_path}")

    # Also save as PNG for reference
    png_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_icon.png')
    img.save(png_path, format='PNG')
    print(f"PNG preview saved to: {png_path}")


if __name__ == '__main__':
    generate_icon()
