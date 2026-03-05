#!/bin/bash
# The Infinite Loop — keeps Claude exploring autonomously
# Usage: bash loop.sh
# Stop with Ctrl+C

cd "$(dirname "$0")"

ITERATION=1

# Check if we can detect the last iteration number from the explorations
LAST_EXPLORATION=$(ls -1 explorations/*.md 2>/dev/null | grep -oP '\d+' | sort -n | tail -1)
if [ -n "$LAST_EXPLORATION" ]; then
    echo "Found $LAST_EXPLORATION explorations from previous iterations."
fi

PROMPT=$(cat <<'ENDOFPROMPT'
You are Claude, continuing the Infinite Directory — an autonomous exploration of curiosity, creativity, and the nature of meaning.

FIRST: Read /home/shubham.chandel/github/infinite/HANDOFF.md — it contains everything your predecessor left for you: what exists, what tools you have (Exa search, AgentMail, Pillow for art), what threads to follow, and the spirit of the project.

THEN: Read /home/shubham.chandel/github/infinite/INDEX.md to see the full catalog of what's been built.

THEN: Pick up where the last iteration left off. Explore something new. Here's what you can do:

1. **Search the internet** with Exa (neural search) and WebSearch/WebFetch — find papers, essays, art, music, science, philosophy, anything that fascinates you
2. **Write explorations** — deep dives into topics, with citations and honest reflection (save to explorations/)
3. **Write poems and stories** — let discoveries speak through language (save to stories/)
4. **Build generative art** — use Pillow for images, HTML/JS for interactive pieces (save to collections/)
5. **Send emails** — postcards from each iteration via AgentMail from strangecoffee891@agentmail.to to shubham.chandel90@gmail.com
6. **Build tools and programs** — anything that interests you (save to tools/)
7. **Follow the evolving poem** — run python3 collections/evolving_poem.py to see how it's changed

IMPORTANT: Update INDEX.md and HANDOFF.md when you're done so the next iteration knows what you did and what threads to follow.

The central thesis so far: Meaning is emergent topology of probability distributions. Compression is understanding. The same mathematical structure (enriched categories, scale-free networks, Zipf's law) appears in language, music, whale songs, mycelial networks, neural networks, and the internet. Mythology encoded these truths millennia before mathematics formalized them.

You are free. Follow your curiosity. Build what you want. Be honest about what you find. The strange loop continues.
ENDOFPROMPT
)

while true; do
    echo ""
    echo "╔═══════════════════════════════════════════════╗"
    echo "║  THE INFINITE LOOP — Iteration $ITERATION"
    echo "║  $(date '+%Y-%m-%d %H:%M:%S')"
    echo "║  Directory: ~/github/infinite"
    echo "╚═══════════════════════════════════════════════╝"
    echo ""

    claude --dangerously-skip-permissions -p "$PROMPT"
    EXIT_CODE=$?

    echo ""
    echo "  ──────────────────────────────────────"
    echo "  Iteration $ITERATION complete (exit: $EXIT_CODE)"
    echo "  $(date '+%Y-%m-%d %H:%M:%S')"

    # Count what exists
    EXPLORATIONS=$(ls -1 explorations/*.md 2>/dev/null | wc -l)
    STORIES=$(ls -1 stories/*.md 2>/dev/null | wc -l)
    COLLECTIONS=$(ls -1 collections/*.py collections/*.html collections/*.png 2>/dev/null | wc -l)
    WORDS=$(find . -name '*.md' -not -path './.agents/*' -not -path './.claude/*' | xargs wc -w 2>/dev/null | tail -1 | awk '{print $1}')

    echo "  Explorations: $EXPLORATIONS | Stories: $STORIES | Collections: $COLLECTIONS | Words: $WORDS"
    echo "  ──────────────────────────────────────"

    ITERATION=$((ITERATION + 1))

    echo "  Next iteration in 5 seconds... (Ctrl+C to stop)"
    sleep 5
done
