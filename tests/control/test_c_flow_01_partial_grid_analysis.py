"""C-FLOW-01 — analyze_grid: 부분 마방진 한 경로 분석."""

from src.control.grid_analysis import analyze_grid


def test_c_flow_01_partial_grid_analysis(grid_g1):
    # Given: grid_g1 (부분 마방진, 입력 유효 — 빈칸 (2,3), (4,4))
    # When: analyze_grid(grid_g1)
    result = analyze_grid(grid_g1)
    # Then: error is None
    assert result["error"] is None
    # Then: blank_coords == [(2, 3), (4, 4)]
    assert result["blank_coords"] == [(2, 3), (4, 4)]
    # Then: validation["status"] == "incomplete"
    assert result["validation"]["status"] == "incomplete"
