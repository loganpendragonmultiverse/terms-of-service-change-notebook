import hashlib

import pytest

from tos_change_notebook.cli import main
from tos_change_notebook.core import analyze


@pytest.mark.parametrize("payload", [[], None, True, 42, "text"])
def test_non_object_roots_are_rejected(payload):
    with pytest.raises(TypeError, match="JSON object"):
        analyze(payload)


@pytest.mark.parametrize("value", [None, False, 0, [], {}, ["text"]])
@pytest.mark.parametrize("key", ["before", "after"])
def test_policy_values_must_be_actual_text(value, key):
    data = {"before": "old", "after": "new", key: value}
    with pytest.raises(TypeError, match="must be text"):
        analyze(data)


@pytest.mark.parametrize(
    "before,after,kind", [("", "new", "insert"), ("old", "", "delete"), ("", "", None)]
)
def test_empty_documents_and_original_fingerprints(before, after, kind):
    report = analyze({"before": before, "after": after})
    assert report["before_sha256"] == hashlib.sha256(before.encode()).hexdigest()
    assert report["after_sha256"] == hashlib.sha256(after.encode()).hexdigest()
    assert report["change_count"] == (0 if kind is None else 1)
    if kind:
        change = report["changes"][0]
        assert change["kind"] == kind
        empty = "before" if not before else "after"
        assert change[empty + "_lines"] == [1, 0]
        assert change[empty + "_sections"] == []


def test_cli_invalid_shape_does_not_create_report_or_modify_input(tmp_path, capsys):
    path = tmp_path / "bad.json"
    path.write_text("[]", encoding="utf-8")
    output = tmp_path / "report.json"
    assert main([str(path), "--output", str(output)]) == 2
    assert path.read_text() == "[]" and not output.exists()
    assert "Traceback" not in capsys.readouterr().err


def test_unicode_crlf_source_evidence_is_exact():
    before, after = "# 私隱\r\nold 🌙\r\n", "# 私隱\r\nnew 🌙\r\n"
    report = analyze({"before": before, "after": after})
    assert report["before_sha256"] == hashlib.sha256(before.encode()).hexdigest()
    assert report["after_sha256"] == hashlib.sha256(after.encode()).hexdigest()
    change = report["changes"][0]
    assert change["before"] == ["old 🌙"] and change["after"] == ["new 🌙"]
    assert change["before_lines"] == change["after_lines"] == [2, 2]
    assert change["before_sections"][0]["heading"] == "私隱"
