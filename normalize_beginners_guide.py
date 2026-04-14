from __future__ import annotations

import argparse
import re
from pathlib import Path


TEXT_REPLACEMENTS = []

SPELL_ELEMENT_RE = re.compile(
    r'(<element\b[^>]*\btype="Spell"[^>]*>)',
    flags=re.IGNORECASE,
)

SOURCE_ATTR_RE = re.compile(r'source="[^"]*"')
ID_ATTR_RE = re.compile(r'id="([^"]*)"')
NON_ALNUM_RE = re.compile(r'[^A-Z0-9]+')


def normalize_spell_id(old_id: str, element_tag: str) -> str:
    if "_SPELL_" in old_id:
        suffix = old_id.split("_SPELL_", 1)[1]
    else:
        name_match = re.search(r'name="([^"]+)"', element_tag)
        if not name_match:
            return old_id
        name = name_match.group(1).upper()
        suffix = NON_ALNUM_RE.sub("_", name).strip("_")

    suffix = NON_ALNUM_RE.sub("_", suffix.upper()).strip("_")
    if not suffix:
        return old_id
    return f"ID_BG_SPELL_{suffix}"


def normalize_spell_element(element_tag: str) -> str:
    updated = SOURCE_ATTR_RE.sub('source="Beginner\'s Guide"', element_tag)

    id_match = ID_ATTR_RE.search(updated)
    if not id_match:
        return updated

    old_id = id_match.group(1)
    new_id = normalize_spell_id(old_id, updated)
    if new_id == old_id:
        return updated

    return ID_ATTR_RE.sub(f'id="{new_id}"', updated, count=1)


def normalize_text(content: str) -> str:
    updated = content
    for old, new in TEXT_REPLACEMENTS:
        updated = updated.replace(old, new)

    # Only normalize Spell elements so Information and other IDs remain stable.
    updated = SPELL_ELEMENT_RE.sub(
        lambda m: normalize_spell_element(m.group(1)),
        updated,
    )

    return updated


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Recursively normalize the Beginner's Guide XML metadata."
    )
    parser.add_argument(
        "--root",
        nargs="?",
        default=str(
            Path(__file__).resolve().parent / "user-faleria" / "beginners-guide" / "spells"
        ),
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