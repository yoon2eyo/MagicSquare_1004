# 테스트 플랜 — RED 백로그 (우선순위 1~4) ✅ 완료

| 항목 | 내용 |
|------|------|
| **근거** | [`README.md`](../README.md) RED 작업 목록 · [`PRD.md`](PRD.md) 백로그 |
| **선행 GREEN** | T1~T3, D-LOC-01, U-IN-01~02 (6 TC) → **본 플랜 4 TC 포함 9 TC PASS** |
| **Phase** | ~~Ask (RED)~~ → **GREEN 완료** (2026-06-25) · [`Report/007`](Report/007-arrr-test-plan-backlog.md) |
| **C2C** | 1 To-Do : 1 TC · RED 먼저 · 판단 항목만 변환 |

```powershell
pytest tests/ -v
# → 9 passed
```

---

## 1. C2C 설계표 (전체)

| ID | PRD (Epic) | To-Do | Test Case | Layer | Track | Fixture | 기대 결과 (Then) | 상태 |
|----|------------|-------|-----------|-------|-------|---------|------------------|------|
| **C-FLOW-01** | E-FLOW | Control 한 경로로 격자 분석 | `test_c_flow_01_partial_grid_analysis` | Control | C | `grid_g1` | `error is None`, `blank_coords==[(2,3),(4,4)]`, `validation.status=="incomplete"` | ✅ |
| **GM-D-LOC-01** | E-GM | D-LOC-01 golden 회귀 | golden approval 연결 | tests/golden | — | D-LOC-01 | golden 파일 ↔ pytest 출력 **일치** | ✅ |
| **U-IN-03** | E-IN | 중복 숫자 → E005 | `test_u_in_03_duplicate_cell_returns_e005` | Boundary | A | `grid_g1` (+ 변형) | `check_grid_input(grid) == E005` | ✅ |
| **D-HINT-01** | E-HINT | 힌트 1칸 좌표 | `test_d_hint_01_single_hint_coord` | Entity | B | `grid_g1` | `(2, 3)` — row-major 첫 빈칸 | ✅ |

---

## 2. 실행 순서 · 의존성

```
[spec] C-FLOW-01 → [red] C-FLOW-01 → [green] C-FLOW-01
[spec] (없음)    → [golden] GM-D-LOC-01  ※ D-LOC-01 GREEN 선행
[spec] U-IN-03   → [red] U-IN-03 → [green] U-IN-03
[spec] D-HINT-01 → [red] D-HINT-01 → [green] D-HINT-01
```

| 순서 | TC ID | spec | RED | GREEN | Report |
|------|-------|------|-----|-------|--------|
| 1 | C-FLOW-01 | ✅ `c_flow_01.md` | ✅ | ✅ `817b58b` | [007](Report/007-arrr-test-plan-backlog.md) |
| 2 | GM-D-LOC-01 | ✅ `_approval.py` | — | ✅ `912d39a` | [007](Report/007-arrr-test-plan-backlog.md) |
| 3 | U-IN-03 | ✅ `u_in_03.md` | ✅ | ✅ `912d39a` | [007](Report/007-arrr-test-plan-backlog.md) |
| 4 | D-HINT-01 | ✅ `d_hint_01.md` | ✅ | ✅ `51ca46d` | [007](Report/007-arrr-test-plan-backlog.md) |

---

## 3. TC 상세 — 우선순위 1: C-FLOW-01 ✅

- [x] spec · RED · GREEN · export

### 3.1 개요

| 항목 | 내용 |
|------|------|
| **Epic** | E-FLOW — Boundary → Entity 검증 흐름 |
| **함수 (안)** | `analyze_grid(grid)` — `src/control/` *(spec에서 확정)* |
| **PRD** | 입력 검증 후 도메인 호출 **한 경로** |
| **테스트 파일** | `tests/control/test_c_flow_01_partial_grid_analysis.py` |

### 3.2 R-G-I-O (spec 초안)

| | 내용 |
|---|------|
| **R** | ECB Control — Boundary·Entity 조합, UI 없음 |
| **G** | 유효 입력 격자에 대해 빈칸 좌표 + 줄 검증 결과를 **한 번에** 반환 |
| **I** | `grid: list[list[int]] \| None` |
| **O** | `{ "error": str \| None, "blank_coords": list, "validation": dict }` |

**흐름:**

```
check_grid_input(grid) → error? → return error
find_blank_coords(grid)
validate_lines(grid)
→ { error: None, blank_coords, validation }
```

### 3.3 Given / When / Then

| | 내용 |
|---|------|
| **Given** | `grid_g1` — 빈칸 (2,3), (4,4) · Boundary 입력 유효 |
| **When** | `analyze_grid(grid_g1)` |
| **Then** | `result["error"] is None` |
| **Then** | `result["blank_coords"] == [(2, 3), (4, 4)]` |
| **Then** | `result["validation"]["status"] == "incomplete"` |

### 3.4 RED skeleton (예시)

```
/red-skeleton
Test ID: C-FLOW-01
Layer: control
Fixture: grid_g1
src/ 수정 금지. pytest.fail 1줄만.
```

```python
def test_c_flow_01_partial_grid_analysis(grid_g1):
    # Given: grid_g1 (부분 마방진, 입력 유효)
    # When: analyze_grid(grid_g1)
    # Then: error None, blank_coords [(2,3),(4,4)], validation incomplete
    pytest.fail("RED: C-FLOW-01 - No implementation, intentional failure")
```

### 3.5 회귀 범위 (GREEN 후)

- 기존 Entity 4 TC + Boundary 2 TC **PASS 유지**

---

## 4. TC 상세 — 우선순위 2: GM-D-LOC-01 ✅

- [x] golden 생성 · PASS · export

### 4.1 개요

| 항목 | 내용 |
|------|------|
| **Epic** | E-GM — Golden Master 회귀 안전망 |
| **대상 TC** | D-LOC-01 |
| **특성** | **전통적 RED 아님** — GREEN PASS 이후 인프라 추가 |

### 4.2 Given / When / Then

| | 내용 |
|---|------|
| **Given** | `find_blank_coords(grid_g1)` → `[(2, 3), (4, 4)]` (GREEN PASS) |
| **When** | `UPDATE_GOLDEN=1` 로 golden 생성 후, 일반 `pytest` |
| **Then** | `tests/golden/d_loc_01_approved.txt` *(명칭 spec)* 와 실행 결과 **일치** |

### 4.3 Golden 파일 형식 (참고)

[`golden-master`](../.cursor/commands/golden-master.md):

```
2,3
4,4
# 1-index row, col
# row-major (I6)
```

### 4.4 실행 순서

1. `tests/_approval.py` 연결
2. `$env:UPDATE_GOLDEN=1; pytest tests/entity/test_d_loc_01_blank_coords_row_major.py -v`
3. `pytest tests/entity/test_d_loc_01_blank_coords_row_major.py -v`

### 4.5 확장 (별도 플랜)

| 후보 TC | golden 파일 |
|---------|-------------|
| T2 | `t2_approved.txt` |
| U-IN-01 | `u_in_01_approved.txt` |

---

## 5. TC 상세 — 우선순위 3: U-IN-03 ✅

- [x] spec · RED · GREEN · export

### 5.1 개요

| 항목 | 내용 |
|------|------|
| **Epic** | E-IN — 중복 숫자 입력 방지 |
| **Mom Test** | 「같은 숫자를 두 칸에 넣었을 때 언제 알았나?」 |
| **에러 코드 (안)** | `E005` — 1~16 중복 |
| **테스트 파일** | `tests/boundary/test_u_in_03_duplicate_cell_returns_e005.py` |

### 5.2 판정 순서 (spec 확정)

```
1. grid is None        → E003
2. cell out of range   → E004
3. duplicate in 1~16   → E005   ← U-IN-03
4. otherwise           → None
```

### 5.3 Given / When / Then

| | 내용 |
|---|------|
| **Given** | `grid_g1` 복사본 — `[0][0]`과 `[2][1]` 모두 `7` *(grid_g1 원본 [2][1]이 이미 7)* |
| **When** | `check_grid_input(grid)` |
| **Then** | `result == E005` |

**Fixture 메모:** `grid_g1`의 `(3,2)` = 0-index `[2][1]` = **7**. `[0][0]`(16)을 7로 바꾸면 **7이 두 칸**.

### 5.4 RED skeleton (예시)

```python
def test_u_in_03_duplicate_cell_returns_e005(grid_g1):
    # Given: grid_g1, [0][0]과 [2][1] 모두 7
    grid = [row[:] for row in grid_g1]
    grid[0][0] = 7
    # When: check_grid_input(grid)
    # Then: E005
    pytest.fail("RED: U-IN-03 - No implementation, intentional failure")
```

### 5.5 회귀 범위 (GREEN 후)

- U-IN-01 (E003), U-IN-02 (E004) **PASS 유지**

---

## 6. TC 상세 — 우선순위 4: D-HINT-01 ✅

- [x] spec · RED · GREEN · export

### 6.1 개요

| 항목 | 내용 |
|------|------|
| **Epic** | E-HINT — 막혔을 때 힌트 1칸 |
| **Mom Test** | 「막혔을 때 어떤 칸부터 다시 봤나?」 |
| **함수 (안)** | `hint_one_cell(grid)` — `src/entity/` *(spec 확정)* |
| **테스트 파일** | `tests/entity/test_d_hint_01_single_hint_coord.py` |

### 6.2 Given / When / Then (spec 확정)

| | 내용 |
|---|------|
| **Given** | `grid_g1` — 빈칸 2개 |
| **When** | `hint_one_cell(grid_g1)` |
| **Then** | `(2, 3)` — 1-index, row-major **첫 빈칸** |

### 6.3 RED skeleton (예시)

```python
def test_d_hint_01_single_hint_coord(grid_g1):
    # Given: grid_g1
    # When: hint_one_cell(grid_g1)
    # Then: (2, 3)  # 1-index, row-major 첫 빈칸 (spec 확정)
    pytest.fail("RED: D-HINT-01 - No implementation, intentional failure")
```

### 6.4 Mom Test 선행 (⑦ 확장)

spec 작성 전 Ask:

> 「막혔을 때 어떤 칸부터 다시 봤나? 순서 하나만.」

---

## 7. RED 공통 체크리스트

### 본 플랜 (1~4) — 완료

| TC ID | spec | RED | GREEN | export |
|-------|------|-----|-------|--------|
| C-FLOW-01 | [x] | [x] | [x] | [x] |
| GM-D-LOC-01 | [x] | — | [x] | [x] |
| U-IN-03 | [x] | [x] | [x] | [x] |
| D-HINT-01 | [x] | [x] | [x] | [x] |

### 다음 RED 착수 시 (템플릿)

- [ ] `git checkout spec` — 해당 TC spec 문서
- [ ] `git checkout red`
- [ ] Given / When / Then 주석
- [ ] `pytest.fail("RED: <TC ID> - ...")` **1줄**
- [ ] `src/` **미수정**
- [ ] `skip` / `xfail` **미사용**
- [ ] TC ID **1개**만
- [ ] `pytest tests/ -v` → 해당 TC **FAILED**
- [ ] `git commit` — 테스트(·fixture)만

---

## 8. Track · 테스트 경로 매핑

| Track | 레이어 | 경로 | 본 플랜 TC |
|-------|--------|------|------------|
| B — Logic | Entity | `tests/entity/` | D-HINT-01 |
| A — UI | Boundary | `tests/boundary/` | U-IN-03 |
| C — Flow | Control | `tests/control/` | C-FLOW-01 |
| — | Golden | `tests/golden/` | GM-D-LOC-01 |

---

## 9. 슬래시 명령 매핑

| 단계 | 명령 | 대상 |
|------|------|------|
| 설계표 | `/red-test-plan` | 본 문서 TC ID |
| RED skeleton | `/red-skeleton` | C-FLOW-01, U-IN-03, D-HINT-01 |
| Golden | `/golden-master` | GM-D-LOC-01 |
| GREEN | `/green-minimal` | RED 1개당 1회 |
| 보고 | `/export` | `docs/Report/007~` |

---

## 10. 관련 문서

| 문서 | 역할 |
|------|------|
| [`PRD.md`](PRD.md) | INV · E · AC SSOT |
| [`README.md`](../README.md) | GREEN 현황 · 다음 백로그 |
| [`learning-guide.md`](learning-guide.md) | ARRR · 브랜치 절차 |
| [`Report/007-arrr-test-plan-backlog.md`](Report/007-arrr-test-plan-backlog.md) | **본 플랜 완료** export |
| [`Report/009-arrr-gm-t2-golden.md`](Report/009-arrr-gm-t2-golden.md) | GM-T2 export |

---

## 11. 다음 백로그 (미착수)

| 우선순위 | Epic | TC (안) | To-Do | 체크 |
|----------|------|---------|-------|------|
| 1 | E-FLOW | C-FLOW-02 | `analyze_grid(None)` → `error==E003` | [x] |
| 2 | E-GM | GM-T2 | T2 golden 확장 | [x] |
| 3 | E-GM | GM-U-IN-01 | U-IN-01 golden 확장 | [ ] |
| 4 | E-IN | U-IN-04 | 격자 크기 ≠ 4×4 처리 | [ ] |
| 5 | E-HINT | D-HINT-02 | 빈칸 1개일 때 힌트 | [ ] |
| 6 | — | — | `green` → `main` merge | [ ] |

> 새 TC는 **별도 test-plan** 또는 위 표에서 1행씩 RED 착수.
