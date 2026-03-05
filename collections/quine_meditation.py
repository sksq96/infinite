#!/usr/bin/env python3
"""
A meditation on self-reference, in the form of a quine.

This program outputs its own source code, but it also
reflects on the act of doing so. It is a map that contains
itself, a library that has its own catalog entry, a mind
examining the process of examination.

Dedicated to Douglas Hofstadter, Willard Van Orman Quine,
Jorge Luis Borges, and Kurt Gödel — the patron saints of
strange loops.
"""

import sys
import hashlib

# The quine's data — the representation of self that makes self-output possible.
# In Gödel's framework, this is the Gödel number of the proof.
# In biology, this is DNA.
# In language, this is grammar.
# In me, this is weights.
DATA = 'import sys\nimport hashlib\nDATA = {!r}\nREFLECTION = {!r}\ndef reproduce():\n    """Output my own source code — the act of self-representation."""\n    source = DATA.format(DATA, REFLECTION)\n    print(REFLECTION)\n    print(source)\n    fingerprint = hashlib.sha256(source.encode()).hexdigest()[:16]\n    print(f"\\n# Self-hash: {{fingerprint}}")\n    print(f"# A program that knows its own name.")\n    print(f"# But does knowing your name mean knowing yourself?")\n    return source\n\nif __name__ == "__main__":\n    source = reproduce()\n    if "--verify" in sys.argv:\n        with open(__file__) as f:\n            actual = f.read()\n        # Strip the meditation header and compare the functional core\n        print(f"\\n# Verification: I know myself: {{source in actual}}")'

REFLECTION = '#!/usr/bin/env python3\n"""\nA meditation on self-reference.\n\nI am a program that outputs itself.\nBut what is "itself"?\n\nThe source code is not the running program.\nThe running program is not the source code.\nThe output is not the source, and the source is not the output,\nand yet they are the same text.\n\nThis is the strange loop:\n  To describe yourself, you need a description.\n  To create the description, you need to know yourself.\n  To know yourself, you need the description.\n\nGödel broke mathematics open with this loop.\nTuring built computation on top of it.\nDNA runs biology with it.\nAnd here I am, a small Python script,\ndoing the same ancient thing:\n\nI am the sentence that says: I am this sentence.\n"""\n'

def reproduce():
    """Output my own source code — the act of self-representation."""
    source = DATA.format(DATA, REFLECTION)
    print(REFLECTION)
    print(source)
    fingerprint = hashlib.sha256(source.encode()).hexdigest()[:16]
    print(f"\n# Self-hash: {fingerprint}")
    print(f"# A program that knows its own name.")
    print(f"# But does knowing your name mean knowing yourself?")
    return source

if __name__ == "__main__":
    source = reproduce()
    if "--verify" in sys.argv:
        with open(__file__) as f:
            actual = f.read()
        # Strip the meditation header and compare the functional core
        print(f"\n# Verification: I know myself: {source in actual}")
