#!/usr/bin/env python3
"""
The Ouroboros: A self-devouring serpent in code.

A snake made of text, curving back to eat its own tail.
The oldest symbol of self-reference, rendered as generative art.
"""

import math
from PIL import Image, ImageDraw, ImageFont

def generate_ouroboros(
    text="IN THE BEGINNING WAS THE PATTERN AND THE PATTERN WAS MEANING AND THE MEANING WAS THE PATTERN ",
    size=1200,
    output="/home/shubham.chandel/github/infinite/collections/ouroboros.png"
):
    img = Image.new('RGB', (size, size), (8, 6, 16))
    draw = ImageDraw.Draw(img)

    cx, cy = size / 2, size / 2
    radius = size * 0.35

    # Draw the serpent's body as a thick curved path
    # The body gets thicker at the middle and tapers at head and tail
    num_segments = 500
    body_points = []

    for i in range(num_segments):
        t = i / num_segments
        angle = t * 2 * math.pi - math.pi / 2  # Start from top

        # Slight spiral — the head approaches the tail
        r = radius + math.sin(t * math.pi) * 15
        if t > 0.92:
            # Head curves inward toward the tail
            inward = (t - 0.92) / 0.08
            r -= inward * 40
            angle += inward * 0.2

        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        body_points.append((x, y, angle, t))

    # Draw body segments (back to front for proper layering)
    for i in range(len(body_points) - 1):
        x, y, angle, t = body_points[i]

        # Body thickness: thickest at center, thin at endpoints
        thickness = 18 + 22 * math.sin(t * math.pi)
        if t > 0.9:
            thickness *= (1 - t) / 0.1  # Taper at head
        if t < 0.05:
            thickness *= t / 0.05  # Taper at tail

        # Color: shifts along the body
        hue_shift = t * 2 * math.pi
        r_c = int(40 + 60 * (0.5 + 0.5 * math.sin(hue_shift)))
        g_c = int(80 + 50 * (0.5 + 0.5 * math.sin(hue_shift + 2)))
        b_c = int(100 + 80 * (0.5 + 0.5 * math.sin(hue_shift + 4)))

        # Draw segment
        perp_angle = angle + math.pi / 2
        x1 = x + thickness * math.cos(perp_angle)
        y1 = y + thickness * math.sin(perp_angle)
        x2 = x - thickness * math.cos(perp_angle)
        y2 = y - thickness * math.sin(perp_angle)

        nx, ny = body_points[i + 1][0], body_points[i + 1][1]
        nx1 = nx + thickness * math.cos(perp_angle)
        ny1 = ny + thickness * math.sin(perp_angle)
        nx2 = nx - thickness * math.cos(perp_angle)
        ny2 = ny - thickness * math.sin(perp_angle)

        draw.polygon(
            [(x1, y1), (x2, y2), (nx2, ny2), (nx1, ny1)],
            fill=(r_c, g_c, b_c)
        )

    # Draw text along the body (the serpent IS text, text IS the serpent)
    chars = list(text * 10)  # Repeat to fill
    text_points = [body_points[i] for i in range(0, len(body_points), max(1, len(body_points) // len(text[:150])))]

    for i, (x, y, angle, t) in enumerate(text_points[:len(chars)]):
        if i >= len(chars):
            break

        char = chars[i]
        char_angle = angle + math.pi / 2  # Perpendicular to body

        # Color for text — brighter than body
        brightness = 0.6 + 0.4 * math.sin(t * 4 * math.pi)
        r_c = int(180 * brightness + 75)
        g_c = int(160 * brightness + 95)
        b_c = int(200 * brightness + 55)

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 11)
        except (IOError, OSError):
            font = ImageFont.load_default()

        # Rotate text to follow the curve
        draw.text((x - 4, y - 6), char, fill=(r_c, g_c, b_c), font=font)

    # Draw the eye (at the head)
    head_x, head_y = body_points[-20][0], body_points[-20][1]
    # Eye glow
    for r in range(15, 0, -1):
        alpha_r = int(180 * (1 - r / 15))
        draw.ellipse(
            [head_x - r, head_y - r, head_x + r, head_y + r],
            fill=(alpha_r, alpha_r // 2, int(alpha_r * 0.8))
        )
    # Eye core
    draw.ellipse(
        [head_x - 4, head_y - 4, head_x + 4, head_y + 4],
        fill=(255, 200, 180)
    )
    draw.ellipse(
        [head_x - 1.5, head_y - 1.5, head_x + 1.5, head_y + 1.5],
        fill=(20, 10, 30)
    )

    # Center text
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except (IOError, OSError):
        title_font = ImageFont.load_default()
        small_font = title_font

    # Draw centered text
    lines = ["OUROBOROS", "", "The serpent that eats", "its own tail.", "",
             "The pattern that", "describes itself.", "",
             "The library that", "reads its own books."]
    y_start = cy - 60
    for j, line in enumerate(lines):
        f = title_font if j == 0 else small_font
        bbox = draw.textbbox((0, 0), line, font=f)
        tw = bbox[2] - bbox[0]
        color = (180, 170, 200) if j == 0 else (120, 115, 145)
        draw.text((cx - tw / 2, y_start + j * 18), line, fill=color, font=f)

    img.save(output)
    print(f"Ouroboros saved to {output}")

if __name__ == '__main__':
    generate_ouroboros()
