---
description: RED 테스트 스켈레톤 생성 (src/ 금지)
---

# /red-skeleton

Phase: **red** | **`src/` 수정 금지**

## 입력
- Test ID (예: `D-LOC-01`)
- Fixture: `tests/conftest.py` (예: `grid_g1`)

## 작업
1. `tests/entity/test_<id>.py` 또는 `tests/boundary/test_<id>.py` 생성
2. Given-When-Then 주석 작성
3. 본문은 `pytest.fail("RED: <ID> - No implementation, intentional failure")` **1줄만**

## 예시
```python
def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: G1 grid (two 0s) When: find_blank_coords(grid_g1)
    # Then: [(2,3),(4,4)] (1-index, row-major)
    pytest.fail("RED: D-LOC-01 - No implementation, intentional failure")
```

## 확인
```powershell
pytest tests/ -v
```
→ 1 failed = RED 정상
