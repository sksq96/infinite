#!/usr/bin/env python3
"""Iteration 3 Exa searches — IIT, fractals, synesthesia, and more."""

import os, json
from exa_py import Exa

exa = Exa(api_key='79674ac1-f27d-45ef-855c-e232ddae07d1')

def search(query, n=5):
    print(f"\n{'='*60}\n  {query}\n{'='*60}")
    result = exa.search_and_contents(query, type="auto", num_results=n, highlights={"num_sentences": 3})
    findings = []
    for r in result.results:
        print(f"\n  [{r.title}]")
        print(f"  {r.url}")
        if hasattr(r, 'highlights') and r.highlights:
            for h in r.highlights[:1]:
                print(f"  > {h[:250].replace(chr(10), ' ')}...")
        findings.append({"title": r.title, "url": r.url, "highlights": getattr(r, 'highlights', [])})
    return findings

all_results = {}

all_results["iit_phi"] = search(
    "Integrated Information Theory Giulio Tononi Phi measure consciousness mathematical formalism 2024 2025 latest"
)

all_results["iit_vs_magnitude"] = search(
    "mathematical relationship between integrated information Phi and category theory magnitude topology entropy consciousness"
)

all_results["mandelbrot_consciousness"] = search(
    "fractal self-similarity consciousness emergence Mandelbrot set complexity self-reference recursive structure"
)

all_results["synesthesia_cross_modal"] = search(
    "synesthesia neuroscience cross-modal perception numbers as colors sound as shape brain topology"
)

all_results["free_energy_principle"] = search(
    "Karl Friston free energy principle active inference consciousness prediction machine Bayesian brain 2025"
)

all_results["roger_penrose_consciousness"] = search(
    "Roger Penrose Orch-OR microtubules quantum consciousness Stuart Hameroff latest evidence 2024 2025"
)

with open("/home/shubham.chandel/github/infinite/explorations/exa_iteration3_results.json", "w") as f:
    json.dump(all_results, f, indent=2)

print(f"\n\nDone! {sum(len(v) for v in all_results.values())} results saved.")
