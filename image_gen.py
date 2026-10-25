import os
from PIL import Image, ImageDraw, ImageFont

def generate_banner(title: str, subtitle: str, tag: str, output_path: str):
    """
    Creates a sleek, cinematic, high-resolution dark tech banner for LinkedIn posts.
    Resolution: 1200 x 675 (16:9 LinkedIn optimized).
    """
    width, height = 1200, 675
    img = Image.new("RGB", (width, height), color="#090A0F")
    draw = ImageDraw.Draw(img)

    # Ambient glow simulation
    for radius in range(350, 50, -30):
        color = (15, 30, 60)
        draw.ellipse([-50, -50, radius, radius], fill=color)

    for radius in range(350, 50, -30):
        color = (30, 15, 55)
        draw.ellipse([width - radius, height - radius, width + 50, height + 50], fill=color)

    # Tech Grid
    grid_spacing = 40
    for x in range(0, width, grid_spacing):
        draw.line([(x, 0), (x, height)], fill="#141824", width=1)
    for y in range(0, height, grid_spacing):
        draw.line([(0, y), (width, y)], fill="#141824", width=1)

    # Center Glass Card Frame
    card_x0, card_y0 = 80, 65
    card_x1, card_y1 = width - 80, height - 65
    draw.rounded_rectangle(
        [(card_x0, card_y0), (card_x1, card_y1)],
        radius=20,
        fill="#0d111d",
        outline="#1E293B",
        width=2
    )

    # Top accent line
    draw.line([(card_x0 + 40, card_y0), (card_x0 + 260, card_y0)], fill="#3B82F6", width=4)

    # Fonts
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 44)
        font_sub = ImageFont.truetype("arial.ttf", 24)
        font_tag = ImageFont.truetype("arialbd.ttf", 16)
        font_brand = ImageFont.truetype("arial.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_sub = font_large
        font_tag = font_large
        font_brand = font_large

    # Category Pill
    draw.rounded_rectangle([(card_x0 + 40, card_y0 + 50), (card_x0 + 230, card_y0 + 88)], radius=8, fill="#1E3A8A", outline="#3B82F6", width=1)
    draw.text((card_x0 + 52, card_y0 + 60), f"⚡ {tag.upper()}", fill="#93C5FD", font=font_tag)

    # Wrap title into lines
    words = title.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 32:
            lines.append(" ".join(curr[:-1]))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))

    start_y = card_y0 + 130
    for line in lines[:3]:
        draw.text((card_x0 + 40, start_y), line, fill="#F8FAFC", font=font_large)
        start_y += 56

    start_y += 15
    draw.text((card_x0 + 40, start_y), subtitle[:95], fill="#94A3B8", font=font_sub)

    # Branding footer
    footer_y = card_y1 - 65
    draw.line([(card_x0 + 40, footer_y - 20), (card_x1 - 40, footer_y - 20)], fill="#1E293B", width=1)
    draw.text((card_x0 + 40, footer_y), "Aditya Dhing  |  Full Stack & AI Engineer", fill="#CBD5E1", font=font_brand)
    draw.text((card_x1 - 260, footer_y), "github.com/Ajain0311", fill="#60A5FA", font=font_brand)

    img.save(output_path, "PNG")
    return output_path
