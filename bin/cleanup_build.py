#!/usr/bin/env python
"""
A simple script to clean up Python build artifacts from the current directory.
Removes 'build/', 'dist/', and any '*.egg-info/' directories or files.
"""
import shutil
from pathlib import Path

# Patterns for items to delete
PATTERNS_TO_DELETE = ["build", "dist", "*.egg-info"]


def main():
    """
    Finds and removes specified build artifacts from the current working directory.
    """
    print("Starting cleanup of build artifacts...")
    current_dir = Path.cwd()
    items_removed_count = 0

    for pattern in PATTERNS_TO_DELETE:
        for path_item in current_dir.glob(pattern):
            try:
                if path_item.is_dir():
                    print(f"Removing directory: {path_item.relative_to(current_dir)}")
                    shutil.rmtree(path_item)
                    items_removed_count += 1
                elif path_item.is_file():
                    print(f"Removing file: {path_item.relative_to(current_dir)}")
                    path_item.unlink()
                    items_removed_count += 1
            except Exception as e:
                print(f"Error removing {path_item.relative_to(current_dir)}: {e}")

    if items_removed_count > 0:
        print(f"Successfully removed {items_removed_count} item(s).")
    else:
        print("No build artifacts found to remove.")
    print("Cleanup finished.")


if __name__ == "__main__":
    main()
