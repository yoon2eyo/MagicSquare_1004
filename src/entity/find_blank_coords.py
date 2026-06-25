"""빈칸(0) 좌표 찾기 — Entity."""

from src.entity.constants import BLANK_CELL, GRID_SIZE


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    coords: list[tuple[int, int]] = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == BLANK_CELL:
                coords.append((r + 1, c + 1))
    return coords
