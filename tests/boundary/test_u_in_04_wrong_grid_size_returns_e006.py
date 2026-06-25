"""U-IN-04 — check_grid_input: 격자 크기 ≠ 4×4 → E006."""

import pytest


def test_u_in_04_wrong_grid_size_returns_e006():
    # Given: 3×4 격자 (행 3개, 열 4개)
    grid = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]
    # When: check_grid_input(grid)
    # Then: E006
    pytest.fail("RED: U-IN-04 - No implementation, intentional failure")
