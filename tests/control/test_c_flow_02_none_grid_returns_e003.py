"""C-FLOW-02 — analyze_grid: grid=None → E003."""

from src.boundary.error_codes import E003
from src.control.grid_analysis import analyze_grid


def test_c_flow_02_none_grid_returns_e003():
    # Given: grid=None
    # When: analyze_grid(None)
    result = analyze_grid(None)
    # Then: error == E003
    assert result["error"] == E003
    # Then: blank_coords [], validation {}
    assert result["blank_coords"] == []
    assert result["validation"] == {}
