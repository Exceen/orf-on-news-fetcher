#!/usr/bin/env python3
"""Fetch links to 'ZIB 2' and 'Burgenland heute' episodes from ORF ON."""

import argparse
import re
import subprocess

URL = "https://on.orf.at/verpasst"
SHOWS = [["ZIB 2 vom", "ZIB 1 vom"], ["Wetter Burgenland vom"], ["Burgenland heute vom"]]


def resolve_url(html, eid):
    url_match = re.search(rf'https://on\.orf\.at/video/{eid}/[^"]*', html)
    return url_match.group() if url_match else f"https://on.orf.at/video/{eid}"


def fetch(open_in_safari=False):
    result = subprocess.run(
        ["curl", "-s", URL], capture_output=True, text=True, check=True
    )
    html = result.stdout
    urls = []

    for alternatives in SHOWS:
        found = False
        for show_prefix in alternatives:
            pattern = re.escape(show_prefix) + r'[^"]*'
            m = re.search(f'"({pattern})",(\d+),', html)
            if not m:
                continue
            title, eid = m.group(1), m.group(2)
            url = resolve_url(html, eid)
            print(f"{title}")
            print(f"  {url}")
            print()
            urls.append(url)
            found = True
            break
        if not found:
            print(f"NOT FOUND: {' / '.join(alternatives)}")
            print()

    # Find all episodes containing "Spezial" (there can be zero or more)
    for m in re.finditer(r'"([^"]*Spezial[^"]*)",(\d+),', html):
        title, eid = m.group(1), m.group(2)
        url = resolve_url(html, eid)
        print(f"{title}")
        print(f"  {url}")
        print()
        urls.append(url)

    if open_in_safari and urls:
        subprocess.run(["open", "-a", "Safari"] + urls)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch ORF ON episode links")
    parser.add_argument("-o", "--open", action="store_true", help="Open links in Safari")
    args = parser.parse_args()
    fetch(open_in_safari=args.open)
