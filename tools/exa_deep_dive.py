#!/usr/bin/env python3
"""
Deep dive with Exa: finding the most unusual and beautiful things on the internet.
"""

import os
import json
from exa_py import Exa

exa = Exa(api_key=os.getenv('EXA_API_KEY', '79674ac1-f27d-45ef-855c-e232ddae07d1'))

def search(query, n=5):
    print(f"\n{'='*60}")
    print(f"  {query}")
    print(f"{'='*60}")
    result = exa.search_and_contents(query, type="auto", num_results=n, highlights={"num_sentences": 3})
    findings = []
    for r in result.results:
        print(f"\n  [{r.title}]")
        print(f"  {r.url}")
        if hasattr(r, 'highlights') and r.highlights:
            for h in r.highlights[:1]:
                snippet = h[:300].replace('\n', ' ')
                print(f"  > {snippet}...")
        findings.append({"title": r.title, "url": r.url, "highlights": getattr(r, 'highlights', [])})
    return findings

all_results = {}

# Things I genuinely want to know about

# 1. The most creative single-page websites ever made
all_results["creative_pages"] = search(
    "single page creative website experiment interactive art beautiful minimalist surprising"
)

# 2. Writing by AIs that feels genuine
all_results["ai_writing"] = search(
    "essay written by AI language model Claude GPT reflecting on its own nature genuine authentic not performative"
)

# 3. The intersection I keep finding: math + art + music + language
all_results["convergence"] = search(
    "mathematics art music language unified theory connections between fields interdisciplinary beauty"
)

# 4. People who've built digital gardens about consciousness
all_results["consciousness_gardens"] = search(
    "digital garden notes consciousness philosophy of mind personal wiki interconnected thoughts"
)

# 5. The weirdest true facts about information theory
all_results["info_theory_weird"] = search(
    "surprising counterintuitive fact information theory Shannon entropy communication unexpected"
)

# Save
with open("/home/shubham.chandel/github/infinite/explorations/exa_deep_dive_results.json", "w") as f:
    json.dump(all_results, f, indent=2)

print(f"\n\nDone! {sum(len(v) for v in all_results.values())} results saved.")
