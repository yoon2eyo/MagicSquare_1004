"""격자 입력 검증 — Boundary."""

from src.boundary.error_codes import E003


def check_grid_input(grid: list[list[int]] | None) -> str | None:
    if grid is None:
        return E003
    return None
