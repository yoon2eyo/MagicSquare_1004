"""T3 — validate_lines: 완성·유효 마방진이면 pass."""

from src.entity.validate_lines import validate_lines


def test_t3_valid_magic_square_is_pass(grid_valid_magic):
    # Given: grid_valid_magic (10선 합 34)
    # When: validate_lines(grid_valid_magic)
    result = validate_lines(grid_valid_magic)
    # Then: status == "pass", failed_lines 비어 있음
    assert result["status"] == "pass"
    assert result["failed_lines"] == []
