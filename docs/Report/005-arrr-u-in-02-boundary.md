# ARRR 1사이클 보고 — 005

| 항목 | 내용 |
|------|------|
| **일자** | 2026-06-25 |
| **Track** | A — Boundary |
| **TC ID** | U-IN-02 |
| **브랜치 흐름** | `spec` → `red` → `green` |

---

## 1. 이번 사이클 요약

### spec — `spec` · `6d0fe00`

- **산출:** [`docs/spec/u_in_02.md`](../spec/u_in_02.md)
- **계약:** 유효 범위 밖 셀 → `E004` (`0` 또는 `1~16`만 허용)

### Ask (RED) — `red` · `10b6887`

- **Given:** `grid_g1`에서 `[0][0]` 값 `17`로 변경
- **Then:** `check_grid_input(grid) == E004`
- **산출:** `tests/boundary/test_u_in_02_out_of_range_cell_returns_e004.py` (`pytest.fail`)

### Respond (GREEN) — `green`

- **변경:** `src/boundary/error_codes.py` — `E004` 추가
- **변경:** `src/boundary/grid_input.py` — 범위 검증 (`BLANK_CELL`, `1~GRID_SIZE²`)
- **변경:** `pytest.fail` → `assert`

### Refine (REFACTOR)

| 판정 |
|------|
| 신규 스멜 없음 — **REFACTOR 생략** |

---

## 2. pytest 결과 (채팅 기록만)

### RED

```
pytest tests/boundary/test_u_in_02_out_of_range_cell_returns_e004.py -v
→ 1 failed — RED: U-IN-02
```

### GREEN

```
pytest tests/ -v
→ 5 passed
test_u_in_01_none_grid_returns_e003 PASSED
test_u_in_02_out_of_range_cell_returns_e004 PASSED
test_t1 · test_t2 · test_t3 PASSED
```

---

## 3. `check_grid_input` 판정 순서 (갱신)

```
1. grid is None     → E003
2. cell out of range → E004
3. otherwise        → None
```

### 다음 RED 후보

| ID | Track | To-Do |
|----|-------|-------|
| **D-LOC-01** | B — Entity | `find_blank_coords(grid_g1)` → `[(2,3),(4,4)]` |

---

## 관련 커밋

| 단계 | 커밋 | 메시지 |
|------|------|--------|
| spec | `6d0fe00` | spec: U-IN-02 check_grid_input out-of-range E004 contract |
| red | `10b6887` | red: U-IN-02 out-of-range cell returns E004 skeleton |
| green | (GREEN) | green: U-IN-02 check_grid_input returns E004 for out-of-range cell |
