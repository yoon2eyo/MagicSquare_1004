"""T3 — validate_lines: 완성·유효 마방진이면 pass."""

import pytest


def test_t3_valid_magic_square_is_pass(grid_valid_magic):
    # Given: grid_valid_magic (10선 합 34)
    # When: validate_lines(grid_valid_magic)
    # Then: status == "pass", failed_lines 비어 있음
    pytest.fail("RED: T3 - No implementation, intentional failure")
