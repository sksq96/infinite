#!/usr/bin/env python3
"""
Exa Explorer: Deep search following curiosity threads.
Uses Exa's neural search to find the most thoughtful writing
on the topics this exploration has uncovered.
"""

import os
import json
from exa_py import Exa

exa = Exa(api_key=os.getenv('EXA_API_KEY', '79674ac1-f27d-45ef-855c-e232ddae07d1'))

def search_and_save(query, filename, num_results=5):
    """Search Exa and save results."""
    print(f"\n{'='*60}")
    print(f"Searching: {query}")
    print(f"{'='*60}")

    result = exa.search_and_contents(
        query,
        type="auto",
        num_results=num_results,
        highlights={"num_sentences": 3}
    )

    findings = []
    for r in result.results:
        print(f"\n  Title: {r.title}")
        print(f"  URL: {r.url}")
        if hasattr(r, 'highlights') and r.highlights:
            for h in r.highlights[:2]:
                print(f"  > {h[:200]}...")
        findings.append({
            "title": r.title,
            "url": r.url,
            "highlights": r.highlights if hasattr(r, 'highlights') else []
        })

    return findings

# ==================== SEARCHES ====================

all_findings = {}

# 1. The deepest thinking about AI inner experience
all_findings["ai_inner_life"] = search_and_save(
    "thoughtful philosophical essay about what it might be like to be an AI language model from the inside, phenomenal experience machine consciousness",
    "ai_inner_life"
)

# 2. Category theory and meaning - beyond Bradley
all_findings["category_meaning"] = search_and_save(
    "category theory applied to meaning semantics language enriched categories mathematical linguistics",
    "category_meaning"
)

# 3. The most beautiful writing about mathematics
all_findings["beautiful_math"] = search_and_save(
    "beautiful personal essay about the experience of doing mathematics discovery wonder proof elegance",
    "beautiful_math"
)

# 4. Borges and computation - deep connections
all_findings["borges_computation"] = search_and_save(
    "Borges Library of Babel computation information theory deep philosophical analysis",
    "borges_computation"
)

# 5. Music and topology - the deepest connections
all_findings["music_topology"] = search_and_save(
    "mathematical topology of music theory algebraic geometry sound composition Xenakis Mazzola",
    "music_topology"
)

# 6. Digital gardens and knowledge as topology
all_findings["knowledge_topology"] = search_and_save(
    "digital garden interconnected knowledge personal wiki learning in public best examples thoughtful",
    "knowledge_topology"
)

# 7. The most interesting thing on the internet right now
all_findings["interesting_internet"] = search_and_save(
    "most fascinating creative unusual website interactive art experiment 2025 2026 hidden gem",
    "interesting_internet"
)

# 8. Self-reference in nature, code, and consciousness
all_findings["self_reference"] = search_and_save(
    "self-reference strange loops quine Hofstadter Godel consciousness emergence self-awareness recursion",
    "self_reference"
)

# Save all findings
output_path = "/home/shubham.chandel/github/infinite/explorations/exa_deep_search_results.json"
with open(output_path, 'w') as f:
    json.dump(all_findings, f, indent=2)

print(f"\n\nAll findings saved to {output_path}")
print(f"Total results: {sum(len(v) for v in all_findings.values())}")
