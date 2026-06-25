"""Golden Master approval — UPDATE_GOLDEN=1 로 기준 파일 갱신."""

import os
from pathlib import Path

_GOLDEN_DIR = Path(__file__).parent / "golden"


def assert_matches_golden(golden_id: str, actual: str) -> None:
    path = _GOLDEN_DIR / f"{golden_id}_approved.txt"
    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(actual, encoding="utf-8")
        return

    expected = path.read_text(encoding="utf-8")
    assert _data_lines(actual) == _data_lines(expected)


def _data_lines(text: str) -> list[str]:
    return [line for line in text.strip().splitlines() if line and not line.lstrip().startswith("#")]


def format_coords(coords: list[tuple[int, int]]) -> str:
    lines = [f"{r},{c}" for r, c in coords]
    lines.append("# 1-index row, col")
    lines.append("# row-major (I6)")
    return "\n".join(lines) + "\n"
