"""격자 입력 검증 — Boundary."""

from src.boundary.error_codes import E003, E004, E005
from src.entity.constants import BLANK_CELL, GRID_SIZE


def check_grid_input(grid: list[list[int]] | None) -> str | None:
    if grid is None:
        return E003

    max_cell = GRID_SIZE * GRID_SIZE
    seen: set[int] = set()
    for row in grid:
        for cell in row:
            if cell != BLANK_CELL and not (1 <= cell <= max_cell):
                return E004
            if cell != BLANK_CELL:
                if cell in seen:
                    return E005
                seen.add(cell)

    return None
