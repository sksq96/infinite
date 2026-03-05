#!/usr/bin/env python3
"""Send iMessages via BlueBubbles private API."""

import argparse
import requests
import sys

API_URL = "https://rouge-optical-award-three.trycloudflare.com/api/v1/message/text"
PASSWORD = "thisisasafepassword"
DEFAULT_CHAT_GUID = "any;-;+15512297529"


def send(message: str, chat_guid: str = DEFAULT_CHAT_GUID) -> dict:
    resp = requests.post(
        API_URL,
        params={"password": PASSWORD},
        json={"chatGuid": chat_guid, "message": message, "method": "private-api"},
    )
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(description="Send an iMessage")
    parser.add_argument("message", help="Text to send")
    parser.add_argument("--to", default=DEFAULT_CHAT_GUID, help="Chat GUID (default: %(default)s)")
    args = parser.parse_args()

    try:
        result = send(args.message, args.to)
        print(f"Sent: {args.message}")
        print(f"Response: {result}")
    except requests.RequestException as e:
        print(f"Failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
