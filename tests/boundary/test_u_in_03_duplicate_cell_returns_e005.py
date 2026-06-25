"""U-IN-03 — check_grid_input: 중복 숫자 → E005."""

from src.boundary.error_codes import E005
from src.boundary.grid_input import check_grid_input


def test_u_in_03_duplicate_cell_returns_e005(grid_g1):
    # Given: grid_g1, [0][0]과 [2][1] 모두 7
    grid = [row[:] for row in grid_g1]
    grid[0][0] = 7
    # When: check_grid_input(grid)
    result = check_grid_input(grid)
    # Then: E005
    assert result == E005
