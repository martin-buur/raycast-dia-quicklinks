# Dia Bookmarks to Raycast Quicklinks

A [Raycast](https://www.raycast.com) script command that imports your [Dia](https://www.diabrowser.com) bookmarks as Raycast quicklinks.

Raycast root search does not show browser bookmarks. To open a bookmark, you first open a bookmark search command and then search again. Quicklinks do show in root search, so after the import you type part of a bookmark name and press Enter.

## Requirements

- macOS with Python 3. The `python3` that comes with the Xcode Command Line Tools is sufficient.
- Raycast v2. Tested with Raycast 2.7.2.
- Dia. Tested with Dia 1.52.0.

## Install

1. Download the script into a folder for Raycast script commands and make it executable. This example uses `~/Raycast/scripts`:

   ```sh
   mkdir -p ~/Raycast/scripts
   curl -o ~/Raycast/scripts/sync-dia-bookmarks.py https://raw.githubusercontent.com/martin-buur/raycast-dia-quicklinks/main/sync-dia-bookmarks.py
   chmod +x ~/Raycast/scripts/sync-dia-bookmarks.py
   ```

2. In Raycast Settings, go to Script Commands and add the folder.

## Usage

1. In Raycast, run **Sync Dia Bookmarks to Quicklinks**.
2. The first time, Raycast asks if it can open the command from a link. Select **Always Open Command**.
3. Raycast opens **Import Quicklinks** with your bookmarks. Press Enter to import.

Run the command again after you add bookmarks in Dia. The import skips bookmarks whose URL is already a quicklink, so it only adds the new ones.

Each quicklink opens in Dia and shows the site's favicon.

## Configuration

To leave folders out of the import, edit `EXCLUDE_FOLDERS` at the top of the script:

```python
EXCLUDE_FOLDERS = ["Shopping", "Random"]
```

To preview the import data without opening Raycast, run:

```sh
./sync-dia-bookmarks.py --dry-run
```

## Limitations

- **Add only.** If you rename or delete a bookmark in Dia, the quicklink does not change. Edit or delete it in Raycast.
- **Deleted quicklinks come back.** If you delete an imported quicklink in Raycast, the next sync adds it again. To prevent this, delete the bookmark in Dia or exclude its folder.
- **Changed URLs make duplicates.** If a bookmark URL changes, the next sync adds a second quicklink.
- **Default profile only.** The script reads bookmarks from the Dia profile named `Default`.
- **Undocumented Raycast deeplink.** The script opens `raycast://extensions/raycast/quicklinks/import-quicklinks` with the bookmarks in the `context` parameter. Raycast does not document this deeplink, so a Raycast update can break it. It is not tested with Raycast v1.

## How it works

Dia is based on Chromium and keeps its bookmarks in a JSON file:

```
~/Library/Application Support/Dia/User Data/Default/Bookmarks
```

The script converts each bookmark to the Raycast quicklink import format and opens the Import Quicklinks command with that data. Raycast stores quicklinks in an encrypted database, so the import is the only way to add many quicklinks at once.

## License

[MIT](LICENSE)
