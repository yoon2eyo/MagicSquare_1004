"""D-LOC-01 — find_blank_coords: grid_g1 빈칸 좌표."""

from tests._approval import assert_matches_golden, format_coords
from src.entity.find_blank_coords import find_blank_coords


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: grid_g1 (빈칸 2개)
    # When: find_blank_coords(grid_g1)
    result = find_blank_coords(grid_g1)
    # Then: [(2, 3), (4, 4)] (1-index, row-major)
    assert result == [(2, 3), (4, 4)]
    assert_matches_golden("d_loc_01", format_coords(result))
