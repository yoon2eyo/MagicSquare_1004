# spec — U-IN-04: 격자 크기 ≠ 4×4 → E006

| 항목 | 내용 |
|------|------|
| **TC ID** | U-IN-04 |
| **Epic** | E-IN |
| **함수** | `check_grid_input` 확장 |
| **선행** | U-IN-01~03 GREEN |

---

## R-G-I-O

| | 내용 |
|---|------|
| **R** | ECB Boundary — `GRID_SIZE` 불변식 검증 |
| **G** | 4×4가 아닌 격자는 셀 검사 전에 거부 |
| **I** | `grid: list[list[int]]` (None 아님) |
| **O** | `E006` 또는 `None` |

## 판정 순서

1. `grid is None` → E003
2. `len(grid) ≠ GRID_SIZE` 또는 행 길이 ≠ `GRID_SIZE` → **E006**
3. cell out of range → E004
4. duplicate in 1~16 → E005
5. otherwise → None

## AC

| | 내용 |
|---|------|
| **Given** | 3×4 격자 (행 3개, 열 4개) |
| **When** | `check_grid_input(grid)` |
| **Then** | `result == E006` |

## RED

| 항목 | 값 |
|------|-----|
| 테스트 | `tests/boundary/test_u_in_04_wrong_grid_size_returns_e006.py` |
| 본문 | `pytest.fail("RED: U-IN-04 - ...")` 1줄 · `src/` 수정 금지 |

## 관련

- [`docs/PRD.md`](../PRD.md) INV-D3 · `GRID_SIZE`
- [`u_in_03.md`](u_in_03.md) — 선행 판정 순서
