"""U-IN-03 — check_grid_input: 중복 숫자 → E005."""

import pytest


def test_u_in_03_duplicate_cell_returns_e005(grid_g1):
    # Given: grid_g1, [0][0]과 [2][1] 모두 7
    grid = [row[:] for row in grid_g1]
    grid[0][0] = 7
    # When: check_grid_input(grid)
    # Then: E005
    pytest.fail("RED: U-IN-03 - No implementation, intentional failure")
