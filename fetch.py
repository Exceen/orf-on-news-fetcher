#!/usr/bin/env python3
"""Fetch links to 'ZIB 2' and 'Burgenland heute' episodes from ORF ON."""

import re
import subprocess

URL = "https://on.orf.at/verpasst"
SHOWS = [["ZIB 2 vom", "ZIB 1 vom"], ["Burgenland heute vom"]]


def fetch():
    result = subprocess.run(
        ["curl", "-s", URL], capture_output=True, text=True, check=True
    )
    html = result.stdout

    for alternatives in SHOWS:
        found = False
        for show_prefix in alternatives:
            pattern = re.escape(show_prefix) + r'[^"]*'
            m = re.search(f'"({pattern})",(\d+),', html)
            if not m:
                continue
            title, eid = m.group(1), m.group(2)
            url_match = re.search(rf'https://on\.orf\.at/video/{eid}/[^"]*', html)
            if url_match:
                print(f"{title}")
                print(f"  {url_match.group()}")
            else:
                print(f"{title}")
                print(f"  https://on.orf.at/video/{eid}")
            print()
            found = True
            break
        if not found:
            print(f"NOT FOUND: {' / '.join(alternatives)}")
            print()

    
    # Find all "ZIB Spezial" episodes (there can be zero or more)
    # Payload format: "Title",EPISODE_ID,... and URL: on.orf.at/video/EPISODE_ID/slug
    for m in re.finditer(r'"(Spezial[^"]*)",(\d+),', html):
        title, eid = m.group(1), m.group(2)
        url_match = re.search(rf'https://on\.orf\.at/video/{eid}/[^"]*', html)
        if url_match:
            print(f"{title}")
            print(f"  {url_match.group()}")
        else:
            print(f"{title}")
            print(f"  https://on.orf.at/video/{eid}")
        print()


if __name__ == "__main__":
    fetch()
