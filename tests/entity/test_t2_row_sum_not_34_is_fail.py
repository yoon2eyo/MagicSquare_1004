"""T2 — validate_lines: 완성 격자에서 한 칸 틀리면 fail + failed_lines."""

import pytest


def test_t2_row_sum_not_34_is_fail(grid_complete):
    # Given: grid_complete, 1-index (2,2) = 0-index [1][1] 값 11→12 변경
    grid = [row[:] for row in grid_complete]
    grid[1][1] = 12
    # When: validate_lines(grid)
    # Then: status="fail", "R2" and "C2" in failed_lines
    pytest.fail("RED: T2 - No implementation, intentional failure")
