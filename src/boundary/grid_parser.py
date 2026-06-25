"""웹 폼 → 4×4 격자 변환."""

from src.entity.constants import BLANK_CELL, GRID_SIZE


def parse_grid_from_form(cells: list[str]) -> list[list[int]]:
    """16개 셀 문자열을 row-major 4×4 격자로 변환. 빈칸 → BLANK_CELL."""
    if len(cells) != GRID_SIZE * GRID_SIZE:
        raise ValueError(f"expected {GRID_SIZE * GRID_SIZE} cells")

    values: list[int] = []
    for raw in cells:
        text = raw.strip()
        if text == "":
            values.append(BLANK_CELL)
            continue
        values.append(int(text))

    grid: list[list[int]] = []
    for row in range(GRID_SIZE):
        start = row * GRID_SIZE
        grid.append(values[start : start + GRID_SIZE])
    return grid


def grid_to_form_values(grid: list[list[int]] | None) -> list[str]:
    """격자를 폼 입력값 16개로 변환. BLANK_CELL → 빈 문자열."""
    if grid is None:
        return [""] * (GRID_SIZE * GRID_SIZE)

    cells: list[str] = []
    for row in grid:
        for cell in row:
            cells.append("" if cell == BLANK_CELL else str(cell))
    return cells
