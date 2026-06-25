"""T1 — validate_lines: 빈칸 있으면 incomplete."""

import pytest


def test_t1_blank_grid_is_incomplete(grid_g1):
    # Given: grid_g1 (빈칸 2개 — 1-index (2,3), (4,4))
    # When: validate_lines(grid_g1)
    # Then: status == "incomplete"
    pytest.fail("RED: T1 - No implementation, intentional failure")
