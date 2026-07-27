from __future__ import annotations

import difflib
import hashlib
import json
from collections import Counter
from typing import Any

PROJECT = "terms-of-service-change-notebook"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _tos_notebook(data: dict[str, Any]) -> dict[str, Any]:
    before = str(_require(data, "before"))
    after = str(_require(data, "after"))
    before_lines, after_lines = (before.splitlines(), after.splitlines())
    changes = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
        None, before_lines, after_lines
    ).get_opcodes():
        if tag == "equal":
            continue
        old, new = (before_lines[i1:i2], after_lines[j1:j2])
        combined = " ".join(old + new).casefold()
        category = next(
            (
                name
                for name, words in {
                    "privacy": ("privacy", "data", "tracking"),
                    "billing": ("price", "payment", "refund", "subscription"),
                    "rights": ("license", "ownership", "content", "copyright"),
                    "disputes": ("arbitration", "court", "law", "dispute"),
                    "termination": ("terminate", "suspend", "delete"),
                }.items()
                if any(word in combined for word in words)
            ),
            "other",
        )
        changes.append(
            {
                "kind": tag,
                "category": category,
                "before_lines": [i1 + 1, i2],
                "after_lines": [j1 + 1, j2],
                "before": old,
                "after": new,
            }
        )
    return {
        "changes": changes,
        "change_count": len(changes),
        "by_category": dict(Counter(item["category"] for item in changes)),
        "before_sha256": hashlib.sha256(before.encode()).hexdigest(),
        "after_sha256": hashlib.sha256(after.encode()).hexdigest(),
    }


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    return {"version": 1, "project": PROJECT, **_tos_notebook(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.extend(
                [
                    f"## {key.replace('_', ' ').title()}",
                    "",
                    f"```json\n{json.dumps(value, indent=2, ensure_ascii=False, default=str)}\n```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"
