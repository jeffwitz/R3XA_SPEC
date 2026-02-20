#!/usr/bin/env python3
"""Generate schema.json from schema-full.json by stripping editorial keys."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_INPUT = Path("schema-full.json")
DEFAULT_OUTPUT = Path("schema.json")
STRIP_KEYS = {"$comment", "examples", "rationale", "see", "notes"}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate schema.json from schema-full.json by stripping non-runtime keys."
    )
    parser.add_argument("source", nargs="?", default=str(DEFAULT_INPUT), help="Input schema path")
    parser.add_argument("output", nargs="?", default=str(DEFAULT_OUTPUT), help="Output schema path")
    return parser.parse_args()


def _strip_keys(value: Any) -> tuple[Any, int]:
    if isinstance(value, dict):
        stripped = 0
        result: dict[str, Any] = {}
        for key, item in value.items():
            if key in STRIP_KEYS:
                stripped += 1
                continue
            cleaned_item, removed = _strip_keys(item)
            result[key] = cleaned_item
            stripped += removed
        return result, stripped
    if isinstance(value, list):
        result: list[Any] = []
        stripped = 0
        for item in value:
            cleaned_item, removed = _strip_keys(item)
            result.append(cleaned_item)
            stripped += removed
        return result, stripped
    return value, 0


def _byte_size(path: Path) -> int:
    if not path.exists():
        return 0
    return path.stat().st_size


def main() -> None:
    args = _parse_args()
    source = Path(args.source)
    output = Path(args.output)

    schema = json.loads(source.read_text(encoding="utf-8"))
    cleaned, stripped = _strip_keys(schema)

    output.parent.mkdir(parents=True, exist_ok=True)
    before = _byte_size(source)
    output.write_text(json.dumps(cleaned, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    after = _byte_size(output)

    if stripped == 0:
        print(
            f"schema.json written ({before - after} bytes stripped; warning: no STRIP_KEYS found in source)"
        )
    else:
        print(f"schema.json written ({before - after} bytes stripped)")


if __name__ == "__main__":
    main()
