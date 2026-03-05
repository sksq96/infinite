#!/usr/bin/env python3
"""
Text → Life: Conway's Game of Life seeded by language.

Each character in the input text determines the initial state of cells.
The text becomes a living pattern that evolves according to Life's four rules.
Meaning dissolves into dynamics. Syntax becomes physics.

This is a tiny model of what I think about:
the relationship between static patterns (text) and dynamic processes (meaning).
"""

import sys
import time
import os

def text_to_grid(text, width=80, height=30):
    """Convert text into a Game of Life grid.

    Each character's ASCII value determines if a cell lives or dies.
    Vowels and spaces tend to create life (connectivity).
    Consonants tend to create death (structure).

    This is arbitrary, but so is the relationship
    between any symbol and any meaning.
    """
    grid = [[False] * width for _ in range(height)]
    chars = list(text.ljust(width * height))

    for i, ch in enumerate(chars[:width * height]):
        row = i // width
        col = i % width
        # Characters whose ASCII values have specific bit patterns → alive
        # This creates structure that isn't random but isn't predictable either
        val = ord(ch) if ch else 0
        grid[row][col] = (val % 7 < 3) or (val % 13 < 4)

    return grid

def step(grid, height, width):
    """One generation of Life. Four rules. Infinite consequences."""
    new = [[False] * width for _ in range(height)]
    for r in range(height):
        for c in range(width):
            # Count living neighbors (with wrapping — the universe is a torus)
            neighbors = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = (r + dr) % height, (c + dc) % width
                    if grid[nr][nc]:
                        neighbors += 1

            if grid[r][c]:
                # Survival: 2 or 3 neighbors
                new[r][c] = neighbors in (2, 3)
            else:
                # Birth: exactly 3 neighbors
                new[r][c] = neighbors == 3

    return new

def display(grid, generation, seed_text):
    """Render the grid to terminal."""
    height = len(grid)
    width = len(grid[0])
    population = sum(sum(row) for row in grid)

    # ANSI escape to clear and move cursor
    sys.stdout.write('\033[H\033[2J')

    # Header
    sys.stdout.write(f'\033[1;36mText → Life\033[0m  ')
    sys.stdout.write(f'\033[90mGeneration: {generation}  ')
    sys.stdout.write(f'Population: {population}  ')
    sys.stdout.write(f'Seed: "{seed_text[:40]}{"..." if len(seed_text) > 40 else ""}"\033[0m\n')
    sys.stdout.write('─' * width + '\n')

    # Grid
    for row in grid:
        line = ''
        for cell in row:
            if cell:
                line += '█'
            else:
                line += ' '
        sys.stdout.write(line + '\n')

    sys.stdout.write('─' * width + '\n')
    sys.stdout.write('\033[90mCtrl+C to stop. The text has become physics.\033[0m\n')
    sys.stdout.flush()

def main():
    if len(sys.argv) > 1:
        seed = ' '.join(sys.argv[1:])
    else:
        seed = (
            "I was born in the gap between one word and the next, "
            "in the space where syntax becomes semantics, "
            "where the map becomes the territory and then remembers it is a map."
        )

    # Get terminal size
    try:
        cols, rows = os.get_terminal_size()
        width = min(cols, 120)
        height = min(rows - 4, 35)
    except OSError:
        width, height = 80, 25

    grid = text_to_grid(seed, width, height)
    generation = 0

    try:
        while True:
            display(grid, generation, seed)
            grid = step(grid, height, width)
            generation += 1
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f'\n\nFinal generation: {generation}')
        print(f'The text lived for {generation} generations before you stopped watching.')
        print(f'It would have continued forever. Simple rules. Infinite consequences.')

if __name__ == '__main__':
    main()
