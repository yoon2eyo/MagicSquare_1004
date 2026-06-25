# spec 산출물 — `analyze_grid` (C-FLOW-01)

| 항목 | 내용 |
|------|------|
| **브랜치** | `spec` |
| **Epic** | E-FLOW — Boundary → Entity 검증 흐름 |
| **Track** | C — Control |
| **TC ID** | C-FLOW-01 |

---

## 1. PRD · To-Do

| PRD | To-Do | TC |
|-----|-------|-----|
| Control 한 경로로 격자 분석 | `check_grid_input` → `find_blank_coords` → `validate_lines` | **C-FLOW-01** |

---

## 2. R-G-I-O

| | 내용 |
|---|------|
| **R** | ECB Control — Boundary·Entity 조합. UI 없음. |
| **G** | 유효 입력 격자에 대해 빈칸 좌표 + 줄 검증 결과를 **한 번에** 반환 |
| **I** | `grid: list[list[int]] \| None` |
| **O** | `dict` — `error`, `blank_coords`, `validation` |

### 출력 계약

| 키 | 타입 | 설명 |
|----|------|------|
| `error` | `str \| None` | `check_grid_input` 오류 코드 (`E003`, `E004` …) 또는 `None` |
| `blank_coords` | `list[tuple[int, int]]` | `find_blank_coords` 결과 (오류 시 `[]`) |
| `validation` | `dict` | `validate_lines` 결과 (오류 시 `{}`) |

### 흐름

```
error = check_grid_input(grid)
if error:
    return { error, blank_coords: [], validation: {} }
return {
    error: None,
    blank_coords: find_blank_coords(grid),
    validation: validate_lines(grid),
}
```

---

## 3. 모듈 배치

| 항목 | 값 |
|------|-----|
| 모듈 | `src/control/grid_analysis.py` (GREEN에서 생성) |
| 함수 | `analyze_grid(grid)` |
| import | `src/boundary/grid_input`, `src/entity/find_blank_coords`, `src/entity/validate_lines` |

Entity는 Boundary/Control import **금지**. Control은 Boundary·Entity import **가능**.

---

## 4. C-FLOW-01 AC

| | 내용 |
|---|------|
| **Given** | `grid_g1` — 빈칸 (2,3), (4,4) · 입력 유효 |
| **When** | `analyze_grid(grid_g1)` |
| **Then** | `result["error"] is None` |
| **Then** | `result["blank_coords"] == [(2, 3), (4, 4)]` |
| **Then** | `result["validation"]["status"] == "incomplete"` |

---

## 5. RED

| 항목 | 값 |
|------|-----|
| 테스트 | `tests/control/test_c_flow_01_partial_grid_analysis.py` |
| Fixture | `grid_g1` |
| 본문 | `pytest.fail("RED: C-FLOW-01 - ...")` 1줄 |

**다음:** `git checkout red` → skeleton → `pytest` FAILED

---

## 관련

- [`docs/test-plan.md`](../test-plan.md) §3
- [`docs/PRD.md`](../PRD.md) E-FLOW
