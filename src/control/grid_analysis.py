"""격자 분석 흐름 — Control (Boundary + Entity 조합)."""

from src.boundary.grid_input import check_grid_input
from src.entity.find_blank_coords import find_blank_coords
from src.entity.validate_lines import validate_lines


def analyze_grid(grid: list[list[int]] | None) -> dict[str, object]:
    error = check_grid_input(grid)
    if error is not None:
        return {"error": error, "blank_coords": [], "validation": {}}

    assert grid is not None
    return {
        "error": None,
        "blank_coords": find_blank_coords(grid),
        "validation": validate_lines(grid),
    }
