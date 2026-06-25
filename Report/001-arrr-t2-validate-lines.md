# ARRR 1사이클 보고 — 001

| 항목 | 내용 |
|------|------|
| **일자** | 2026-06-25 |
| **Track** | B — Logic (Entity) |
| **TC ID** | T2 |
| **브랜치 흐름** | `spec` → `red` → `green` |

---

## 1. 이번 사이클 요약

### Ask (RED) — `red` · `155fa0b`

- **대상:** `validate_lines` — 완성 격자에서 한 칸 틀리면 `fail` + `failed_lines`
- **Given:** `grid_complete`, 1-index (2,2) = 0-index `[1][1]` 값 11→12
- **Then:** `status == "fail"`, `"R2"`, `"C2"` ∈ `failed_lines`
- **산출:** `tests/conftest.py` (`grid_complete`), `tests/entity/test_t2_row_sum_not_34_is_fail.py` (`pytest.fail`)

### Respond (GREEN) — `green` · `67eef3a`

- **산출:** `src/entity/validate_lines.py` 최소 구현
- **변경:** `pytest.fail` → `assert` 교체

### Refine (REFACTOR) — `green` · `61aee44`

- **P0:** `_collect_failed_line_ids()` 추출
- **P1:** `_make_result()` 응답 dict 통일
- **계약:** 불변 (`incomplete` / `fail` / `pass` + `failed_lines`)

---

## 2. pytest 결과 (채팅 기록만)

### RED (`red` 브랜치)

```
pytest tests/ -v
→ 1 failed
FAILED tests/entity/test_t2_row_sum_not_34_is_fail.py::test_t2_row_sum_not_34_is_fail
Failed: RED: T2 - No implementation, intentional failure
```

### GREEN (`green` 브랜치)

```
pytest tests/ -v
→ 1 passed
tests/entity/test_t2_row_sum_not_34_is_fail.py::test_t2_row_sum_not_34_is_fail PASSED
```

### REFACTOR 후 (`green` 브랜치)

```
pytest tests/ -v
→ 1 passed
tests/entity/test_t2_row_sum_not_34_is_fail.py::test_t2_row_sum_not_34_is_fail PASSED
```

> Golden Master: 미설정 — 채팅에 검증 기록 없음.

---

## 3. 다음 RED 후보

| ID | To-Do | Given | Then |
|----|-------|-------|------|
| **T1** | 빈칸 있으면 incomplete | `grid_g1` (빈칸 2개) | `status == "incomplete"` |

**브랜치:** `git checkout red` → `/red-skeleton` Test ID: T1

---

## 관련 커밋

| 단계 | 커밋 | 메시지 |
|------|------|--------|
| spec | `fca0b4e` | docs: align T2 RED example with spec coordinates |
| red | `155fa0b` | red: T2 validate_lines fail skeleton with grid_complete fixture |
| green | `67eef3a` | green: T2 validate_lines fail with failed_lines for R2 and C2 |
| refactor | `61aee44` | refactor: extract failed line collection and result helper in validate_lines |

## Mom Test → 계약 연결 (참고)

> **진짜 문제:** 부분 마방진을 채우는 동안 10개 줄의 합(34)을 즉시 판정하고, 틀린 줄을 바로 알 수 없어 확인에 시간이 낭비된다.

T2는 `fail` + `failed_lines`(R2, C2)로 「틀린 줄을 바로 알 수 없음」을 해결하는 첫 구현이다.
