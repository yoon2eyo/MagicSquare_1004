"""D-HINT-02 — hint_one_cell: 빈칸 1개일 때 유일한 좌표."""

from src.entity.hint_one_cell import hint_one_cell


def test_d_hint_02_one_blank_hint_coord(grid_g1_one_blank):
    # Given: grid_g1_one_blank — 빈칸 (4,4)만 남음
    # When: hint_one_cell(grid_g1_one_blank)
    result = hint_one_cell(grid_g1_one_blank)
    # Then: (4, 4)
    assert result == (4, 4)
