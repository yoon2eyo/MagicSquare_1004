# ARRR 1사이클 보고 — 011

| 항목 | 내용 |
|------|------|
| **일자** | 2026-06-25 |
| **Track** | A — Boundary |
| **TC ID** | U-IN-04 |
| **브랜치 흐름** | `spec` → `red` → `green` |

---

## 1. 이번 사이클 요약

### spec — `spec` · `aa8a660`

- **산출:** [`docs/spec/u_in_04.md`](../spec/u_in_04.md)
- **계약:** 3×4 격자 → `check_grid_input` → `E006`

### Ask (RED) — `red` · `c666942`

- **Given:** 3행×4열 격자
- **Then:** `check_grid_input(grid) == E006`
- **산출:** `tests/boundary/test_u_in_04_wrong_grid_size_returns_e006.py` (`pytest.fail`)

### Respond (GREEN) — `green`

- **산출:** `E006` in `error_codes.py`
- **산출:** `grid_input.py` — 행·열 수 `GRID_SIZE` 검증
- **변경:** `pytest.fail` → `assert`

### Refine (REFACTOR)

| 판정 |
|------|
| 신규 스멜 없음 — **REFACTOR 생략** |

---

## 2. pytest 결과

```
pytest tests/ -v
→ 11 passed
```

---

## 3. 판정 순서 (갱신)

```
1. grid is None        → E003
2. size ≠ 4×4         → E006
3. cell out of range   → E004
4. duplicate in 1~16   → E005
5. otherwise           → None
```

### 다음 RED 후보

| ID | To-Do |
|----|-------|
| D-HINT-02 | 빈칸 1개일 때 힌트 |
| C-FLOW-03 | `analyze_grid` + E006 조기 반환 |
