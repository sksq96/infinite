#!/usr/bin/env python3
"""Quick notification helper — sends iMessage updates."""

import sys
sys.path.insert(0, "/home/shubham.chandel/github/infinite/tools")
from imessage import send

def notify(msg):
    """Send a short iMessage update."""
    try:
        send(msg)
        print(f"iMessage sent: {msg[:80]}...")
    except Exception as e:
        print(f"iMessage failed: {e}")

if __name__ == "__main__":
    notify(" ".join(sys.argv[1:]) if len(sys.argv) > 1 else "ping from the Infinite Directory")
