"""U-IN-01 — check_grid_input: grid=None → E003."""
"""U-IN-01 — check_grid_input: grid=None → E003."""
2
​
 |  | 
3
 
6
 
from tests._approval import assert_matches_golden, format_error_code
7
 
from src.boundary.error_codes import E003
8
 
from src.boundary.grid_input import check_grid_input
9
 
10
​
11
​
12
def test_u_in_01_none_grid_returns_e003():
13
    # Given: grid=None
14
    # When: check_grid_input(None)
 |  | 
15
 
19
 
    result = check_grid_input(None)
20
 
    # Then: E003
21
 
    assert result == E003
22
 
    assert_matches_golden("u_in_01", format_error_code(result))
23
 
24

from tests._approval import assert_matches_golden, format_error_code
from src.boundary.error_codes import E003
from src.boundary.grid_input import check_grid_input


def test_u_in_01_none_grid_returns_e003():
    # Given: grid=None
    # When: check_grid_input(None)
    result = check_grid_input(None)
    # Then: E003
    assert result == E003
    assert_matches_golden("u_in_01", format_error_code(result))
