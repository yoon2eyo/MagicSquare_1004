"""D-HINT-01 — hint_one_cell: row-major 첫 빈칸."""

from src.entity.hint_one_cell import hint_one_cell


def test_d_hint_01_single_hint_coord(grid_g1):
    # Given: grid_g1
    # When: hint_one_cell(grid_g1)
    result = hint_one_cell(grid_g1)
    # Then: (2, 3) — 1-index, row-major 첫 빈칸
    assert result == (2, 3)
