# spec 산출물 — `analyze_grid` 오류 경로 (C-FLOW-02)

| 항목 | 내용 |
|------|------|
| **브랜치** | `spec` |
| **Epic** | E-FLOW — Boundary → Entity 검증 흐름 |
| **Track** | C — Control |
| **TC ID** | C-FLOW-02 |
| **선행** | C-FLOW-01 GREEN · U-IN-01 GREEN |

---

## 1. PRD · To-Do

| PRD | To-Do | TC |
|-----|-------|-----|
| Control 오류 격자 조기 반환 | `grid=None` → `error==E003`, Entity 미호출 | **C-FLOW-02** |

---

## 2. R-G-I-O

| | 내용 |
|---|------|
| **R** | ECB Control — C-FLOW-01 오류 분기 **명시 검증** |
| **G** | `None` 입력 시 Boundary 오류만 반환, 도메인 결과 없음 |
| **I** | `grid=None` |
| **O** | `{ "error": "E003", "blank_coords": [], "validation": {} }` |

### 흐름 (C-FLOW-01 계약 §2 재사용)

```
error = check_grid_input(grid)   # None → E003
if error:
    return { error, blank_coords: [], validation: {} }
# Entity 호출 없음
```

---

## 3. C-FLOW-02 AC

| | 내용 |
|---|------|
| **Given** | `grid=None` |
| **When** | `analyze_grid(None)` |
| **Then** | `result["error"] == E003` |
| **Then** | `result["blank_coords"] == []` |
| **Then** | `result["validation"] == {}` |

---

## 4. RED

| 항목 | 값 |
|------|-----|
| 테스트 | `tests/control/test_c_flow_02_none_grid_returns_e003.py` |
| Fixture | 없음 |
| 본문 | `pytest.fail("RED: C-FLOW-02 - ...")` 1줄 · `src/` 수정 금지 |

---

## 관련

- [`docs/spec/c_flow_01.md`](c_flow_01.md) — `analyze_grid` 출력 계약
- [`docs/test-plan.md`](../test-plan.md) §11
