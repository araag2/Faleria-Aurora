from __future__ import annotations

import argparse
from pathlib import Path


TEXT_REPLACEMENTS = [
    #("Player’s Handbook", "Beginner's Guide"),
    #("Player's Handbook", "Beginner's Guide"),
    ("ID_FALERIA_PHB24_", "ID_WOTC_PHB24_"),
    #("ID_WOTC_PHB_", "ID_FALERIA_BG_"),
    #("ID_WOTC_", "ID_FALERIA_"),
    ("ID_BG24_", "ID_PHB24_"),
    #("ID_PHB_", "ID_FALERIA_BG_"),
    #("PLAYERS_HANDBOOK", "BEGINNERS_GUIDE"),
    #("PHB.png", "BG.png"),
]


def normalize_text(content: str) -> str:
    updated = content
    for old, new in TEXT_REPLACEMENTS:
        updated = updated.replace(old, new)
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Recursively normalize the Beginner's Guide XML metadata."
    )
    parser.add_argument(
        "--root",
        nargs="?",
        default=str(Path(__file__).resolve().parent / "user-faleria"),
        help="Root folder to process",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Root path does not exist: {root}")

    updated_files = 0

    for path in root.rglob("*"):
        if path.suffix.lower() not in {".xml", ".index"}:
            continue
        original = path.read_text(encoding="utf-8-sig")
        updated = normalize_text(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            updated_files += 1

    print(f"Processed root: {root}")
    print(f"Updated text files: {updated_files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())