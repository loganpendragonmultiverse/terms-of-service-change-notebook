import hashlib

from tos_change_notebook.core import analyze


def test_duplicate_and_renamed_headings_have_separate_source_context():
    before = "# Terms\nintro\n## Data\ncommon\n## Data\nsecond"
    after = "# Terms\nintro\n## Privacy\ncommon\n## Data\nchanged"
    report = analyze({"before": before, "after": after})
    first, second = report["changes"]
    assert first["before_sections"][0]["heading"] == "Data"
    assert first["after_sections"][0]["heading"] == "Privacy"
    section = second["before_sections"][0]
    assert section["heading_line"] == 5 and section["occurrence"] == 2
    assert section["path"] == ["Terms", "Data"]
    assert section["start_line"] == 5 and section["end_line"] == 6


def test_fenced_headings_do_not_create_sections():
    before = "# Real\n```md\n# Fake\nold\n```\n~~~\n## Fake too\n~~~"
    after = before.replace("old", "new")
    report = analyze({"before": before, "after": after})
    assert [s["heading"] for s in report["changes"][0]["before_sections"]] == ["Real"]


def test_unsectioned_ranges_empty_sides_and_fingerprints():
    before, after = "intro\r\nplain", "intro\r\nplain\r\n# Added\r\nbody"
    report = analyze({"before": before, "after": after})
    change = report["changes"][0]
    assert change["before_lines"] == [3, 2]
    assert change["before_sections"] == []
    assert change["after_sections"][0]["heading"] == "Added"
    assert report["before_sha256"] == hashlib.sha256(before.encode()).hexdigest()
    assert report["after_sha256"] == hashlib.sha256(after.encode()).hexdigest()
    unsectioned = analyze({"before": "intro\nold", "after": "intro\nnew"})["changes"][0]
    assert unsectioned["before_sections"][0]["heading"] is None
    assert unsectioned["before_lines"] == [2, 2]
    assert unsectioned["before_sections"][0]["end_line"] == 2


def test_setext_headings_and_changes_spanning_sections():
    before = "Title\n=====\nold\nSub\n---\nold"
    after = "Title\n=====\nnew\nSub\n---\nnew"
    report = analyze({"before": before, "after": after})
    assert report["changes"][0]["before_sections"][0]["path"] == ["Title"]
    assert report["changes"][1]["before_sections"][0]["path"] == ["Title", "Sub"]
    report = analyze({"before": "# A\nx\n# B\ny", "after": "# C\nz"})
    assert [s["heading"] for s in report["changes"][0]["before_sections"]] == ["A", "B"]
