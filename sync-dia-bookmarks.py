#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Sync Dia Bookmarks to Quicklinks
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🔖
# @raycast.packageName Dia
# @raycast.description Open Import Quicklinks prefilled with your Dia bookmarks. Bookmarks that already exist as quicklinks (same URL) are skipped.

import json
import os
import subprocess
import sys
from urllib.parse import quote

BOOKMARKS = os.path.expanduser("~/Library/Application Support/Dia/User Data/Default/Bookmarks")
IMPORT_DEEPLINK = "raycast://extensions/raycast/quicklinks/import-quicklinks"

# Folder names to leave out, for example ["Shopping", "Random"].
EXCLUDE_FOLDERS = []


def walk(node, out, seen):
    if node.get("type") == "folder" and node.get("name") in EXCLUDE_FOLDERS:
        return
    if node.get("type") == "url" and node["url"] not in seen:
        seen.add(node["url"])
        # Raycast shows the site's favicon for quicklinks with the "link" icon.
        # Without an icon, the import falls back to a generic document icon.
        out.append({
            "name": node.get("name") or node["url"],
            "link": node["url"],
            "openWith": "Dia",
            "icon": "link",
        })
    for child in node.get("children", []):
        walk(child, out, seen)


def main():
    with open(BOOKMARKS) as f:
        roots = json.load(f)["roots"]

    quicklinks, seen = [], set()
    for root in roots.values():
        if isinstance(root, dict):
            walk(root, quicklinks, seen)

    url = f"{IMPORT_DEEPLINK}?context={quote(json.dumps(quicklinks, ensure_ascii=False), safe='')}"

    if "--dry-run" in sys.argv:
        print(url)
        return

    # Open the deeplink after this script exits, so Raycast closing its window
    # for a silent script command does not dismiss the import view.
    subprocess.Popen(
        ["/bin/sh", "-c", 'sleep 0.5; open "$0"', url],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


if __name__ == "__main__":
    main()
