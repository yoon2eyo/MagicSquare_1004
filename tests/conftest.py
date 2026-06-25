"""공통 pytest fixture — 격자 G1 등."""

import pytest

# G1: 완성 마방진에서 (2,3)·(4,4) 빈칸(0) — 1-index row-major
_GRID_G1 = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 0],
]

# G1 빈칸 채움 — spec §5.3 grid_complete
_GRID_COMPLETE = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]


@pytest.fixture
def grid_g1():
    """I6: 1-index row-major, 0=빈칸."""
    return [row[:] for row in _GRID_G1]


@pytest.fixture
def grid_complete():
    """완성 격자 — G1 빈칸(2,3)·(4,4)에 10, 1 채움. spec §5.3."""
    return [row[:] for row in _GRID_COMPLETE]
