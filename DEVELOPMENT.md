# Development contract

Categorize differences between two manually saved policy versions with fingerprints.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, changelog, README claims, repository metadata, release assets, and the Forge catalog together.

## 1.1.0 - 2026-10-16

Attach independent before/after Markdown section context to changed source ranges. Distinguish repeated headings by occurrence and line, ignore fenced headings, and retain original fingerprints.

See README.md for interface details and TESTING.md for the verification gate.

## 1.1.1 acceptance

Exercise Unicode/CRLF fingerprints, empty before/after documents, non-object/non-text input, repeated and renamed headings, fenced/setext headings, and exact changed source ranges. Preserve keyword-only, nonlegal interpretation.

Exercise existing/source/dangling/racing destinations, ordinary write failures, complete Unicode stdout and a real consumer-closed pipe. Expect status 2 without a traceback for input/output failures. A failed new write may leave a partial report; tests must preserve every pre-existing file. Run the full configured checks and inspect wheel/source package documents and examples.
