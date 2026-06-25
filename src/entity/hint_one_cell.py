"""힌트 1칸 — row-major 첫 빈칸 좌표."""

from src.entity.find_blank_coords import find_blank_coords


def hint_one_cell(grid: list[list[int]]) -> tuple[int, int]:
    coords = find_blank_coords(grid)
    return coords[0]
