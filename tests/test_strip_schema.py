import json
import subprocess
import sys
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _script_path() -> Path:
    return _project_root() / "tools" / "strip_schema.py"


def _run_strip(source: Path, output: Path) -> str:
    command = [sys.executable, str(_script_path()), str(source), str(output)]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return completed.stdout


def test_strip_removes_comment(tmp_path):
    source = tmp_path / "in.json"
    output = tmp_path / "out.json"
    source.write_text(
        json.dumps({"$comment": "remove", "title": "ok", "nested": {"notes": "x"}}),
        encoding="utf-8",
    )

    _run_strip(source, output)
    data = json.loads(output.read_text(encoding="utf-8"))

    assert "$comment" not in data
    assert "notes" not in data["nested"]
    assert data["title"] == "ok"


def test_strip_removes_nested_keys(tmp_path):
    source = tmp_path / "in.json"
    output = tmp_path / "out.json"
    source.write_text(
        json.dumps(
            {
                "items": [
                    {"examples": [1, 2], "value": 1},
                    {"meta": {"rationale": "x", "keep": True}},
                ]
            }
        ),
        encoding="utf-8",
    )

    _run_strip(source, output)
    data = json.loads(output.read_text(encoding="utf-8"))

    assert "examples" not in data["items"][0]
    assert "rationale" not in data["items"][1]["meta"]
    assert data["items"][1]["meta"]["keep"] is True


def test_strip_preserves_required_fields(tmp_path):
    source = tmp_path / "in.json"
    output = tmp_path / "out.json"
    payload = {
        "type": "object",
        "required": ["title", "version"],
        "properties": {
            "title": {"type": "string"},
            "version": {"const": "2024.7.1"},
        },
    }
    source.write_text(json.dumps(payload), encoding="utf-8")

    _run_strip(source, output)
    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["required"] == ["title", "version"]
    assert data["properties"]["version"]["const"] == "2024.7.1"


def test_strip_no_op_when_nothing_to_strip(tmp_path):
    source = tmp_path / "in.json"
    output = tmp_path / "out.json"
    source.write_text(json.dumps({"title": "unchanged"}), encoding="utf-8")

    stdout = _run_strip(source, output)

    assert "warning: no STRIP_KEYS found" in stdout
    assert json.loads(output.read_text(encoding="utf-8")) == {"title": "unchanged"}


def test_strip_output_is_valid_json(tmp_path):
    source = tmp_path / "in.json"
    output = tmp_path / "out.json"
    source.write_text(
        json.dumps({"description": "ok", "examples": ["drop"], "value": 1}),
        encoding="utf-8",
    )

    _run_strip(source, output)

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["description"] == "ok"
    assert "examples" not in data
