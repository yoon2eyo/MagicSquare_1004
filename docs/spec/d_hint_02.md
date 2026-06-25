# spec — D-HINT-02: 빈칸 1개일 때 힌트

| 항목 | 내용 |
|------|------|
| **TC ID** | D-HINT-02 |
| **Epic** | E-HINT |
| **함수** | `hint_one_cell(grid)` — `src/entity/` |
| **선행** | D-HINT-01 GREEN · D-LOC-01 GREEN |

---

## R-G-I-O

| | 내용 |
|---|------|
| **R** | ECB Entity — 빈칸 1개 남은 부분 마방진 |
| **G** | 유일한 빈칸 좌표를 힌트로 반환 |
| **I** | `grid_g1_one_blank` — 빈칸 1개 (4,4) |
| **O** | `(4, 4)` — 1-index |

## AC

| | 내용 |
|---|------|
| **Given** | `grid_g1_one_blank` — (2,3) 채움, (4,4)만 빈칸 |
| **When** | `hint_one_cell(grid)` |
| **Then** | `(4, 4)` |

## Fixture (`conftest.py`)

`grid_g1`에서 (2,3)에 `10` 채움 — `grid_complete`와 동일 값.

## RED

| 항목 | 값 |
|------|-----|
| 테스트 | `tests/entity/test_d_hint_02_one_blank_hint_coord.py` |
| Fixture | `grid_g1_one_blank` |
| 본문 | `pytest.fail("RED: D-HINT-02 - ...")` 1줄 · `src/` 수정 금지 |

## 관련

- [`d_hint_01.md`](d_hint_01.md) — row-major 첫 빈칸
