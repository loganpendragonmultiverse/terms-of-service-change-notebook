# Terms-of-Service Change Notebook

[![CI](https://github.com/loganpendragonmultiverse/terms-of-service-change-notebook/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/terms-of-service-change-notebook/actions/workflows/ci.yml)

Categorize differences between two manually saved policy versions with fingerprints. The command uses explicit UTF-8 JSON input and produces reviewable JSON or Markdown output.

## Three-minute start

```bash
python -m pip install .
tos-changes examples/sample.json
tos-changes examples/sample.json --format json --output report.json
```

The example documents the v1 input shape. Existing report files are never overwritten. Source inputs are read-only except where the documented purpose explicitly creates a new output artifact.

## Privacy and platforms

The tool runs locally and does not upload input or include telemetry. Python 3.10 or newer is supported on Windows, macOS, and Linux.

## Interpretation boundary

Categories are keyword-based review aids and not legal advice. The tool does not fetch policies or determine legal effect.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Before and after section context

Each change now includes `before_sections` and `after_sections` for the physical source ranges it touches. Sections record heading text, level, outline path, heading line, inclusive section range, and occurrence number for repeated heading text. ATX headings (`# Heading`) and setext headings are recognized outside backtick and tilde fences. Renamed headings retain distinct before/after labels; duplicate titles are distinguished by source location. Unsectioned text has a null heading. An empty side of an insertion/deletion has no section entries, preserving existing range conventions (`[start, start-1]` for an empty range). Source SHA-256 fingerprints and keyword categories are unchanged. This deliberately small Markdown scanner does not model every Markdown dialect or determine legal effect.
