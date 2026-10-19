# Testing

Use an isolated Python environment and install `python -m pip install -e ".[dev]"`.
Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`.
The repository CI matrix covers Python 3.10 and 3.14 on Linux, Windows, and macOS.
New regressions live alongside the existing core/CLI tests.

Setext regressions cover repeated underlines, adjacent thematic breaks, and thematic breaks following bullet/ordered list items, alongside fenced and repeated/renamed headings.

## 1.1.1 acceptance

Exercise Unicode/CRLF fingerprints, empty before/after documents, non-object/non-text input, repeated and renamed headings, fenced/setext headings, and exact changed source ranges. Preserve keyword-only, nonlegal interpretation.

Exercise existing/source/dangling/racing destinations, ordinary write failures, complete Unicode stdout and a real consumer-closed pipe. Expect status 2 without a traceback for input/output failures. A failed new write may leave a partial report; tests must preserve every pre-existing file. Run the full configured checks and inspect wheel/source package documents and examples.
