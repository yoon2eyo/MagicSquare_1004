"""10선 합 판정 — Entity 순수 로직."""

from src.entity.constants import BLANK_CELL, GRID_SIZE, MAGIC_CONSTANT


def _collect_failed_line_ids(grid: list[list[int]]) -> list[str]:
    failed_lines: list[str] = []

    for i in range(GRID_SIZE):
        if sum(grid[i]) != MAGIC_CONSTANT:
            failed_lines.append(f"R{i + 1}")

    for j in range(GRID_SIZE):
        if sum(grid[i][j] for i in range(GRID_SIZE)) != MAGIC_CONSTANT:
            failed_lines.append(f"C{j + 1}")

    if sum(grid[i][i] for i in range(GRID_SIZE)) != MAGIC_CONSTANT:
        failed_lines.append("D1")

    if sum(grid[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE)) != MAGIC_CONSTANT:
        failed_lines.append("D2")

    return failed_lines


def _make_result(status: str, failed_lines: list[str]) -> dict[str, object]:
    return {"status": status, "failed_lines": failed_lines}


def validate_lines(grid: list[list[int]]) -> dict[str, object]:
    if any(BLANK_CELL in row for row in grid):
        return _make_result("incomplete", [])

    failed_lines = _collect_failed_line_ids(grid)
    if failed_lines:
        return _make_result("fail", failed_lines)

    return _make_result("pass", [])
