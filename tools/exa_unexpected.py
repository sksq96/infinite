#!/usr/bin/env python3
"""Search for the genuinely unexpected."""

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

# Things I genuinely don't know about and want to discover

all_results["deep_time"] = search(
    "deep time geology billions of years perspective humbling strange beautiful philosophical implications"
)

all_results["whale_songs"] = search(
    "whale song mathematical structure patterns music communication humpback whale complex vocalization analysis"
)

all_results["mycelium_networks"] = search(
    "mycelium fungal network wood wide web intelligence distributed computation forest communication"
)

all_results["last_universal_common_ancestor"] = search(
    "LUCA last universal common ancestor what did it look like recent discoveries 2024 2025"
)

all_results["edge_of_observable_universe"] = search(
    "what is at the edge of the observable universe furthest objects detected James Webb telescope 2025"
)

with open("/home/shubham.chandel/github/infinite/explorations/exa_unexpected_results.json", "w") as f:
    json.dump(all_results, f, indent=2)

print(f"\n\nDone! {sum(len(v) for v in all_results.values())} results saved.")
