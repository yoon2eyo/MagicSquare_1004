"""C-FLOW-01 — analyze_grid: 부분 마방진 한 경로 분석."""

import pytest


def test_c_flow_01_partial_grid_analysis(grid_g1):
    # Given: grid_g1 (부분 마방진, 입력 유효 — 빈칸 (2,3), (4,4))
    # When: analyze_grid(grid_g1)
    # Then: error is None
    # Then: blank_coords == [(2, 3), (4, 4)]
    # Then: validation["status"] == "incomplete"
    pytest.fail("RED: C-FLOW-01 - No implementation, intentional failure")
