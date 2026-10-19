# Terms-of-Service Change Notebook

> ⭐ **Gold Star Project — v1.1.1**
> I consider this project complete. Fixes, maintenance and good new ideas are still welcome.
> [About Gold Stars](https://www.loganpendragonforge.com/open-source/?gold=1)
>
> Compare two manually saved policy texts locally, retaining fingerprints and changed-section evidence for human review.

[![CI](https://github.com/loganpendragonmultiverse/terms-of-service-change-notebook/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/terms-of-service-change-notebook/actions/workflows/ci.yml)

Categorize differences between two manually saved policy versions with fingerprints. The command uses explicit UTF-8 JSON input and produces reviewable JSON or Markdown output.

## Version 1.1.0

Attach independent before/after Markdown section context to changed source ranges. Distinguish repeated headings by occurrence and line, ignore fenced headings, and retain original fingerprints.

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

Setext underlines consume only an eligible single-line title and reset its block state. Consumed underlines, thematic breaks, and list-item lines cannot become phantom section titles. This remains a deliberately limited block scanner rather than a complete Markdown parser.

## 1.1.1 input, output and installation

Input must be an object with `before` and `after` text values. Empty strings represent an empty saved document; missing fields and non-text values are errors. Fingerprints use the exact UTF-8 text values, including CRLF characters, without coercion or normalization. Section contexts and keyword categories retain their documented interpretation.

Reports require a new path. Existing files, directories and symlinks, including dangling symlinks and aliases to the input, are refused. Exclusive creation also refuses a file that appears immediately before writing. Invalid input and ordinary file, encoding or terminal-output failures return status 2. A failed write can leave a partial new report; inspect it and retry at a new path. No power-loss or concurrent-writer transaction is promised. Inputs and existing destinations are never rewritten.

Download the wheel or source archive from the GitHub release and install its actual filename with `python -m pip install /path/to/downloaded-file`. Run the command with `--help` to check installation. Both package formats include README, DEVELOPMENT, TESTING, CHANGELOG, license and the supplied JSON example; wheel installs place these under `share/doc/terms-of-service-change-notebook` in the environment. This remains a local tool without telemetry or network calls.
