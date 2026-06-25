"""T1 — validate_lines: 빈칸 있으면 incomplete."""

from src.entity.validate_lines import validate_lines


def test_t1_blank_grid_is_incomplete(grid_g1):
    # Given: grid_g1 (빈칸 2개 — 1-index (2,3), (4,4))
    # When: validate_lines(grid_g1)
    result = validate_lines(grid_g1)
    # Then: status == "incomplete"
    assert result["status"] == "incomplete"
