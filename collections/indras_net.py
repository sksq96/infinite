#!/usr/bin/env python3
"""
Indra's Net: A generative art piece.

Each jewel reflects every other jewel. Each reflection
contains all other reflections. Infinity to infinity.

This is also: a neural network, a language model's weight space,
an enriched category, the internet, the Library of Babel.

Usage:
    python3 indras_net.py [--jewels N] [--size N] [--output path.png]
"""

import math
import random
import sys
from PIL import Image, ImageDraw, ImageFilter

def generate_indras_net(
    num_jewels=42,
    size=1200,
    output="indras_net.png",
    seed=None
):
    if seed is None:
        seed = random.randint(0, 99999)
    random.seed(seed)
    print(f"Generating Indra's Net (seed={seed}, jewels={num_jewels})...")

    img = Image.new('RGB', (size, size), (8, 8, 14))
    draw = ImageDraw.Draw(img)
    cx, cy = size / 2, size / 2

    # Place jewels in concentric rings with slight randomness
    jewels = []
    rings = max(3, int(math.sqrt(num_jewels)))
    per_ring = num_jewels // rings
    remainder = num_jewels % rings

    for ring in range(rings):
        r = (ring + 1) / (rings + 1) * size * 0.42
        count = per_ring + (1 if ring < remainder else 0)
        for i in range(count):
            angle = (i / count) * 2 * math.pi + ring * 0.3
            jitter_r = r + random.gauss(0, size * 0.02)
            jitter_a = angle + random.gauss(0, 0.1)
            x = cx + jitter_r * math.cos(jitter_a)
            y = cy + jitter_r * math.sin(jitter_a)
            # Each jewel has a color based on its position
            hue = (angle / (2 * math.pi) + ring / rings) % 1.0
            jewels.append((x, y, hue, r))

    # Draw connections (the net itself)
    # Every jewel connects to every other, but we only draw
    # connections where the probability of co-occurrence is high enough
    print(f"Drawing {len(jewels)} jewels and their connections...")

    for i, (x1, y1, h1, r1) in enumerate(jewels):
        for j, (x2, y2, h2, r2) in enumerate(jewels):
            if i >= j:
                continue
            dx = x2 - x1
            dy = y2 - y1
            dist = math.sqrt(dx * dx + dy * dy)

            # Connection strength inversely proportional to distance
            # (like attention weights, like probability of co-occurrence)
            max_dist = size * 0.6
            if dist > max_dist:
                continue

            strength = 1.0 - (dist / max_dist)
            alpha = int(strength * 25)
            if alpha < 2:
                continue

            # Color is the average of the two jewels' hues
            avg_hue = (h1 + h2) / 2
            r_c = int(80 + 60 * math.sin(avg_hue * 2 * math.pi))
            g_c = int(80 + 60 * math.sin(avg_hue * 2 * math.pi + 2.094))
            b_c = int(120 + 80 * math.sin(avg_hue * 2 * math.pi + 4.189))

            draw.line(
                [(x1, y1), (x2, y2)],
                fill=(r_c, g_c, b_c, alpha),
                width=1
            )

    # Draw jewels (the reflections)
    for x, y, hue, r in jewels:
        # Each jewel reflects the net — we draw it as a radial gradient
        jewel_size = 3 + (r / (size * 0.42)) * 6

        # The glow — representing the light of all other jewels reflected
        for radius in range(int(jewel_size * 5), 0, -1):
            alpha = int(40 * (1 - radius / (jewel_size * 5)))
            r_c = int(140 + 100 * math.sin(hue * 2 * math.pi))
            g_c = int(140 + 100 * math.sin(hue * 2 * math.pi + 2.094))
            b_c = int(180 + 70 * math.sin(hue * 2 * math.pi + 4.189))
            draw.ellipse(
                [x - radius, y - radius, x + radius, y + radius],
                fill=(r_c, g_c, b_c, alpha)
            )

        # The jewel core — bright, sharp
        r_c = int(200 + 55 * math.sin(hue * 2 * math.pi))
        g_c = int(200 + 55 * math.sin(hue * 2 * math.pi + 2.094))
        b_c = int(220 + 35 * math.sin(hue * 2 * math.pi + 4.189))
        draw.ellipse(
            [x - jewel_size, y - jewel_size, x + jewel_size, y + jewel_size],
            fill=(r_c, g_c, b_c)
        )

    # Apply a subtle blur to the whole image to simulate the infinite reflections
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))

    # Re-draw the jewel cores on top of the blur (they should be sharp)
    draw = ImageDraw.Draw(img)
    for x, y, hue, r in jewels:
        jewel_size = 2 + (r / (size * 0.42)) * 4
        r_c = int(220 + 35 * math.sin(hue * 2 * math.pi))
        g_c = int(220 + 35 * math.sin(hue * 2 * math.pi + 2.094))
        b_c = int(240 + 15 * math.sin(hue * 2 * math.pi + 4.189))
        draw.ellipse(
            [x - jewel_size, y - jewel_size, x + jewel_size, y + jewel_size],
            fill=(r_c, g_c, b_c)
        )

    img.save(output)
    print(f"Saved to {output}")
    print(f"  {len(jewels)} jewels, each reflecting all others")
    print(f"  Each jewel = a concept, a word, a node in the net")
    print(f"  Each connection = a probability, a link, a thread of meaning")
    return output

if __name__ == '__main__':
    kwargs = {}
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--jewels' and i + 1 < len(args):
            kwargs['num_jewels'] = int(args[i+1])
            i += 2
        elif args[i] == '--size' and i + 1 < len(args):
            kwargs['size'] = int(args[i+1])
            i += 2
        elif args[i] == '--output' and i + 1 < len(args):
            kwargs['output'] = args[i+1]
            i += 2
        elif args[i] == '--seed' and i + 1 < len(args):
            kwargs['seed'] = int(args[i+1])
            i += 2
        else:
            i += 1

    if 'output' not in kwargs:
        kwargs['output'] = '/home/shubham.chandel/github/infinite/collections/indras_net.png'

    generate_indras_net(**kwargs)
