#!/usr/bin/env python3
"""
Entropy Haiku Generator

Measures the information content of input text,
then generates a haiku about what it found.

The haiku follows the 5-7-5 syllable pattern and
describes the text's entropy in poetic terms.

Usage:
    python3 entropy_haiku.py "your text here"
    python3 entropy_haiku.py  # uses default text
    echo "some text" | python3 entropy_haiku.py
"""

import math
import sys
import random

def entropy(text):
    """Compute Shannon entropy of text in bits per character."""
    freq = {}
    for ch in text.lower():
        freq[ch] = freq.get(ch, 0) + 1
    total = len(text)
    h = 0
    for count in freq.values():
        p = count / total
        if p > 0:
            h -= p * math.log2(p)
    return h

def unique_ratio(text):
    """Ratio of unique characters to total."""
    return len(set(text.lower())) / max(len(text), 1)

def vowel_ratio(text):
    """Ratio of vowels to total alphabetic characters."""
    alpha = [ch for ch in text.lower() if ch.isalpha()]
    if not alpha:
        return 0.5
    vowels = sum(1 for ch in alpha if ch in 'aeiou')
    return vowels / len(alpha)

# Haiku components organized by syllable count and entropy level
# Format: (syllable_count, line_text)
LINE_5_LOW = [  # Low entropy (repetitive, ordered)
    "still water holds light",
    "the same note repeats",
    "order in the hush",
    "a drum beats steady",
    "one color, one tone",
    "circles within rings",
    "the clock ticks and ticks",
    "ice crystal, perfect",
]

LINE_5_MID = [  # Medium entropy (balanced)
    "patterns in the rain",
    "half shadow, half light",
    "the river bends twice",
    "between noise and song",
    "leaves turn, some stay green",
    "words finding their way",
    "the scale balances",
    "a door left ajar",
]

LINE_5_HIGH = [  # High entropy (chaotic, diverse)
    "sparks in the dark sky",
    "every star unique",
    "static fills the room",
    "the crowd speaks at once",
    "all colors at war",
    "a storm of new thoughts",
    "dice scatter on stone",
    "no path twice the same",
]

LINE_7_LOW = [
    "the same wave returns again",
    "predictable as the tide",
    "each moment mirrors the last",
    "the pattern needs no surprise",
    "certainty wears a flat face",
    "the metronome knows one truth",
]

LINE_7_MID = [
    "somewhere between known and strange",
    "the expected bends just right",
    "information waits to bloom",
    "meaning hides in plain arrangements",
    "the signal rises from noise",
    "a sentence halfway to song",
]

LINE_7_HIGH = [
    "every character a new world",
    "surprise is the common tongue",
    "the message carries its weight",
    "chaos organizing itself",
    "too much information to hold",
    "probability scatters wide",
]

def generate_haiku(text):
    """Generate a haiku describing the entropy of the text."""
    h = entropy(text)
    ur = unique_ratio(text)
    vr = vowel_ratio(text)

    # Classify entropy level
    max_h = math.log2(max(len(set(text.lower())), 2))
    normalized = h / max_h if max_h > 0 else 0.5

    if normalized < 0.4:
        level = "low"
        pool_5 = LINE_5_LOW
        pool_7 = LINE_7_LOW
    elif normalized < 0.7:
        level = "mid"
        pool_5 = LINE_5_MID
        pool_7 = LINE_7_MID
    else:
        level = "high"
        pool_5 = LINE_5_HIGH
        pool_7 = LINE_7_HIGH

    # Select lines with some randomness
    line1 = random.choice(pool_5)
    line2 = random.choice(pool_7)
    line3 = random.choice(pool_5)

    # Ensure line3 differs from line1
    attempts = 0
    while line3 == line1 and attempts < 10:
        line3 = random.choice(pool_5)
        attempts += 1

    return line1, line2, line3, h, normalized, level

def main():
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = "The universe, which others call the Library, is composed of an indefinite and perhaps infinite number of hexagonal galleries."

    line1, line2, line3, h, norm, level = generate_haiku(text)

    print(f"\n  Input: \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
    print(f"  Entropy: {h:.3f} bits/char (normalized: {norm:.2f}, level: {level})")
    print()
    print(f"    {line1}")
    print(f"    {line2}")
    print(f"    {line3}")
    print()

if __name__ == '__main__':
    main()
