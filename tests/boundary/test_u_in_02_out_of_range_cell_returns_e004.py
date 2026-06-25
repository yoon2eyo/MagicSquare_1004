"""U-IN-02 — check_grid_input: 범위 밖 숫자 → E004."""

from src.boundary.error_codes import E004
from src.boundary.grid_input import check_grid_input


def test_u_in_02_out_of_range_cell_returns_e004(grid_g1):
    # Given: grid_g1에서 한 칸을 17로 변경 (1~16 밖)
    grid = [row[:] for row in grid_g1]
    grid[0][0] = 17
    # When: check_grid_input(grid)
    result = check_grid_input(grid)
    # Then: E004
    assert result == E004
