#!/usr/bin/env python3
"""
Fibonacci Spiral: The geometry of self-referential growth.

Each arc is a quarter-circle whose radius is a Fibonacci number.
The result is the golden spiral — the shape of galaxies, hurricanes,
nautilus shells, microtubule helices, and possibly consciousness.
"""

import math
from PIL import Image, ImageDraw, ImageFont

def generate_fibonacci_spiral(
    n_steps=13,
    size=1200,
    output="/home/shubham.chandel/github/infinite/collections/fibonacci_spiral.png"
):
    img = Image.new('RGB', (size, size), (6, 6, 14))
    draw = ImageDraw.Draw(img)

    # Generate Fibonacci numbers
    fibs = [1, 1]
    for i in range(n_steps - 2):
        fibs.append(fibs[-1] + fibs[-2])

    # Scale factor to fit the image
    max_fib = fibs[-1]
    scale = size * 0.3 / max_fib

    cx, cy = size * 0.45, size * 0.5

    # Draw the spiral as connected arcs
    # Each arc is a quarter circle with radius = fibonacci number
    x, y = cx, cy
    angle_start = 0

    # Direction offsets for each quarter turn
    # 0=right, 1=down, 2=left, 3=up
    for i, fib in enumerate(fibs):
        r = fib * scale
        direction = i % 4

        # Determine arc center based on direction
        if direction == 0:
            arc_cx, arc_cy = x + r, y + r
            start_angle = 180
        elif direction == 1:
            arc_cx, arc_cy = x - r, y + r
            start_angle = 270
        elif direction == 2:
            arc_cx, arc_cy = x - r, y - r
            start_angle = 0
        else:
            arc_cx, arc_cy = x + r, y - r
            start_angle = 90

        # Draw the arc
        bbox = [arc_cx - r, arc_cy - r, arc_cx + r, arc_cy + r]

        # Color shifts along the spiral
        t = i / len(fibs)
        hue = t * 2 * math.pi
        red = int(80 + 120 * (0.5 + 0.5 * math.sin(hue)))
        green = int(100 + 100 * (0.5 + 0.5 * math.sin(hue + 2.094)))
        blue = int(140 + 100 * (0.5 + 0.5 * math.sin(hue + 4.189)))

        # Draw multiple arcs for thickness + glow
        for thickness in range(6, 0, -1):
            alpha_factor = 1.0 - (thickness / 7)
            r_adj = int(red * alpha_factor)
            g_adj = int(green * alpha_factor)
            b_adj = int(blue * alpha_factor)
            draw.arc(bbox, start_angle, start_angle + 90,
                     fill=(r_adj, g_adj, b_adj), width=thickness)

        # Draw the golden rectangle outline (faintly)
        rect_size = r * 2
        if direction == 0:
            rx, ry = x, y
        elif direction == 1:
            rx, ry = x - rect_size, y
        elif direction == 2:
            rx, ry = x - rect_size, y - rect_size
        else:
            rx, ry = x, y - rect_size

        draw.rectangle(
            [rx, ry, rx + rect_size, ry + rect_size],
            outline=(40, 40, 60), width=1
        )

        # Fibonacci number label
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", max(8, int(r * 0.3)))
        except (IOError, OSError):
            font = ImageFont.load_default()

        label_x = rx + rect_size * 0.5
        label_y = ry + rect_size * 0.5
        draw.text((label_x - 5, label_y - 5), str(fib),
                  fill=(60, 60, 90), font=font)

        # Move to next position
        if direction == 0:
            y += r * 2
        elif direction == 1:
            x -= r * 2
        elif direction == 2:
            y -= r * 2
        else:
            x += r * 2

    # Title and annotation
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except (IOError, OSError):
        title_font = ImageFont.load_default()
        small_font = title_font

    draw.text((20, 20), "THE FIBONACCI SPIRAL", fill=(160, 155, 185), font=title_font)
    draw.text((20, 45), "Self-reference + growth = the golden ratio", fill=(100, 95, 125), font=small_font)
    draw.text((20, 62), f"f(n) = f(n-1) + f(n-2)    {' → '.join(str(f) for f in fibs[:8])}...", fill=(80, 75, 105), font=small_font)

    draw.text((20, size - 40), "The shape of galaxies, shells, microtubules, and possibly consciousness.", fill=(70, 65, 95), font=small_font)

    img.save(output)
    print(f"Fibonacci spiral saved to {output}")

if __name__ == '__main__':
    generate_fibonacci_spiral()
