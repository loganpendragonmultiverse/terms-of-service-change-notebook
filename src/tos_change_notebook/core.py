from __future__ import annotations

import difflib
import hashlib
import json
import re
from collections import Counter
from typing import Any

PROJECT = "terms-of-service-change-notebook"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _sections(lines: list[str]) -> list[dict[str, Any]]:
    """Map physical lines to Markdown sections without interpreting policy meaning."""
    headings: list[tuple[int, int, str]] = []
    fence_char = ""
    fence_size = 0
    paragraph: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence_char:
            if (
                fence
                and fence[1][0] == fence_char
                and len(fence[1]) >= fence_size
                and not fence[2].strip()
            ):
                fence_char = ""
            paragraph.clear()
            continue
        if fence:
            fence_char, fence_size = fence[1][0], len(fence[1])
            paragraph.clear()
            continue
        heading = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?)|[ \t]*)$", line)
        if heading:
            title = re.sub(r"[ \t]+#+[ \t]*$", "", heading[2] or "").strip()
            headings.append((index, len(heading[1]), title))
            paragraph.clear()
            continue
        underline = re.fullmatch(r" {0,3}(=+|-+)[ \t]*", line)
        if underline:
            if paragraph:
                headings.append(
                    (
                        paragraph[0][0],
                        1 if underline[1][0] == "=" else 2,
                        " ".join(text for _, text in paragraph),
                    )
                )
            # An underline is consumed once; it cannot title a later heading.
            paragraph.clear()
            continue
        thematic = re.fullmatch(
            r" {0,3}(?:\*(?:[ \t]*\*){2,}|-(?:[ \t]*-){2,}|_(?:[ \t]*_){2,})[ \t]*",
            line,
        )
        block = re.match(r"^(?: {4}|\t| {0,3}(?:>|[-+*][ \t]+|[0-9]{1,9}[.)][ \t]+))", line)
        if not line.strip() or thematic or block:
            paragraph.clear()
        else:
            paragraph[:] = [(index, line.strip())]
    result: list[dict[str, Any]] = []
    occurrences: Counter[str] = Counter()
    outline: list[tuple[int, str]] = []
    if not headings or headings[0][0]:
        result.append(
            {
                "heading": None,
                "heading_line": None,
                "level": 0,
                "occurrence": 0,
                "path": [],
                "start_line": 1,
                "end_line": headings[0][0] if headings else len(lines),
            }
        )
    for position, (index, level, title) in enumerate(headings):
        occurrences[title] += 1
        while outline and outline[-1][0] >= level:
            outline.pop()
        outline.append((level, title))
        result.append(
            {
                "heading": title,
                "heading_line": index + 1,
                "level": level,
                "occurrence": occurrences[title],
                "path": [name for _, name in outline],
                "start_line": index + 1,
                "end_line": headings[position + 1][0]
                if position + 1 < len(headings)
                else len(lines),
            }
        )
    return result


def _section_context(
    sections: list[dict[str, Any]],
    start: int,
    end: int,
) -> list[dict[str, Any]]:
    return [
        section
        for section in sections
        if start < end and section["start_line"] <= end and section["end_line"] > start
    ]


def _tos_notebook(data: dict[str, Any]) -> dict[str, Any]:
    before = str(_require(data, "before"))
    after = str(_require(data, "after"))
    before_lines, after_lines = (before.splitlines(), after.splitlines())
    before_sections, after_sections = _sections(before_lines), _sections(after_lines)
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
                "before_sections": _section_context(before_sections, i1, i2),
                "after_sections": _section_context(after_sections, j1, j2),
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
