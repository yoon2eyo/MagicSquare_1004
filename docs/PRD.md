# PRD — 4×4 마방진 자동 검증

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_1004 |
| **페르소나** | 부분 마방진(빈칸 2개) 학습자 |
| **아키텍처** | ECB · Dual-Track · C2C · ARRR |
| **격자** | 4×4 (`GRID_SIZE = 4`) |
| **갱신** | 2026-06-25 — **10 TC GREEN** (Entity 5 · Boundary 3 · Control 2 · GM D-LOC-01) |

---

## 문서 구조

| 섹션 | 약어 | 의미 |
|------|------|------|
| **INV** | Investigation + Invariants | Mom Test 조사 · 도메인·아키텍처 불변식 |
| **E** | Epics | 기능 에픽 (PRD 요구 단위) |
| **AC** | Acceptance Criteria | 수용 기준 (Given / When / Then → Test Case) |

추적: **PRD(E) → To-Do → TC(AC)** — C2C 3원칙, 1 To-Do : 1 TC

---

## INV — Investigation + Invariants

### INV-1. Investigation (Mom Test — 진짜 문제)

> **진짜 문제:** 부분 마방진을 채우는 동안 10개 줄의 합(34)을 즉시 판정하고, 틀린 줄을 바로 알 수 없어 확인에 시간이 낭비된다.

| 회차 | 확인된 사실 | 설계·AC 연결 |
|------|-------------|--------------|
| 1 | 행만 확인하고 대각선을 빼먹어 20분 추가 | 10선 전체 검증 (T2, T3) |
| 2 | 행 → 열 → 대각선 순 **부분 검증** | `validate_lines` 10선 한 번에 |
| 3 | 줄 ID 없이 연필 밑줄만 | `failed_lines` (R1~R4, C1~C4, D1, D2) |
| 4 | 빈칸 vs 틀림 구분 불가 | `incomplete` vs `fail` (T1, T2) |

### INV-2. Domain Invariants (도메인 불변식)

| ID | 불변식 | SSOT |
|----|--------|------|
| INV-D1 | 마방진 **10선**(행·열·대각선) 합 = **34** | `MAGIC_CONSTANT` |
| INV-D2 | 빈칸 = **0** | `BLANK_CELL` |
| INV-D3 | 격자 크기 = **4×4** | `GRID_SIZE` |
| INV-D4 | 채워진 칸 값 = **1~16** (빈칸 제외) | Boundary `check_grid_input` |
| INV-D5 | 좌표 표기 = **1-index**, **row-major** | D-LOC-01, D-HINT-01 |
| INV-D6 | `incomplete` 판정 시 10선 합 검사 **하지 않음** | `validate_lines` 우선순위 |
| INV-D7 | 1~16 **중복 없음** (채워진 칸) | U-IN-03 · `E005` |

### INV-3. Architecture Invariants (아키텍처 불변식)

| ID | 불변식 |
|----|--------|
| INV-A1 | Entity는 Boundary/Control **import 금지** |
| INV-A2 | 리터럴 `34`, `0` **하드코딩 금지** — `constants.py`만 |
| INV-A3 | RED: `src/` 수정 금지 · GREEN: 1 RED = 1 커밋 |
| INV-A4 | Dual-Track: Entity → `tests/entity/` · Boundary → `tests/boundary/` · Control → `tests/control/` |

---

## E — Epics (기능 에픽)

| Epic ID | 이름 | Track | 레이어 | 상태 |
|---------|------|-------|--------|------|
| **E-VAL** | 10선 합 즉시 판정 + 실패 줄 표시 | B | Entity | ✅ GREEN |
| **E-LOC** | 빈칸 위치 찾기 | B | Entity | ✅ GREEN |
| **E-HINT** | 힌트 1칸 (row-major 첫 빈칸) | B | Entity | ✅ GREEN |
| **E-IN** | 격자 입력 유효성 (None·범위·중복) | A | Boundary | ✅ GREEN |
| **E-FLOW** | Boundary → Entity 검증 흐름 조합 | C | Control | ✅ GREEN |
| **E-GM** | Golden Master 회귀 안전망 | — | tests/golden | ✅ D-LOC-01 |

### Epic 상세

#### E-VAL — `validate_lines`

- **모듈:** `src/entity/validate_lines.py`
- **출력:** `status` (`incomplete` \| `fail` \| `pass`) + `fail` 시 `failed_lines`
- **spec:** [`docs/spec/validate_lines.md`](spec/validate_lines.md)

#### E-LOC — `find_blank_coords`

- **모듈:** `src/entity/find_blank_coords.py`
- **spec:** [`docs/spec/d_loc_01.md`](spec/d_loc_01.md)

#### E-HINT — `hint_one_cell`

- **모듈:** `src/entity/hint_one_cell.py`
- **출력:** row-major **첫 빈칸** 1-index 좌표
- **spec:** [`docs/spec/d_hint_01.md`](spec/d_hint_01.md)

#### E-IN — `check_grid_input`

- **모듈:** `src/boundary/grid_input.py`, `src/boundary/error_codes.py`
- **오류 코드:** `E003`(None), `E004`(범위 밖), `E005`(중복)
- **spec:** [`docs/spec/u_in_01.md`](spec/u_in_01.md), [`u_in_02.md`](spec/u_in_02.md), [`u_in_03.md`](spec/u_in_03.md)

#### E-FLOW — `analyze_grid`

- **모듈:** `src/control/grid_analysis.py`
- **흐름:** `check_grid_input` → `find_blank_coords` → `validate_lines`
- **spec:** [`docs/spec/c_flow_01.md`](spec/c_flow_01.md)

#### E-GM — Golden Master

- **인프라:** `tests/_approval.py`, `tests/golden/`
- **대상:** D-LOC-01 ✅ · **T2** ✅ (확장: U-IN-01)

---

## AC — Acceptance Criteria (수용 기준)

### Track B — Entity (`tests/entity/`)

| AC ID | Epic | Given | When | Then | TC | 상태 |
|-------|------|-------|------|------|-----|------|
| AC-VAL-02 | E-VAL | `grid_complete`, (2,2) 11→12 | `validate_lines` | `fail`, R2·C2 ∈ failed_lines | T2 | ✅ |
| AC-VAL-01 | E-VAL | `grid_g1` | `validate_lines` | `incomplete` | T1 | ✅ |
| AC-VAL-03 | E-VAL | `grid_valid_magic` | `validate_lines` | `pass` | T3 | ✅ |
| AC-LOC-01 | E-LOC | `grid_g1` | `find_blank_coords` | `[(2,3),(4,4)]` | D-LOC-01 | ✅ |
| AC-HINT-01 | E-HINT | `grid_g1` | `hint_one_cell` | `(2, 3)` | D-HINT-01 | ✅ |

### Track A — Boundary (`tests/boundary/`)

| AC ID | Epic | Given | When | Then | TC | 상태 |
|-------|------|-------|------|------|-----|------|
| AC-IN-01 | E-IN | `grid=None` | `check_grid_input` | `E003` | U-IN-01 | ✅ |
| AC-IN-02 | E-IN | `grid_g1`, [0][0]=17 | `check_grid_input` | `E004` | U-IN-02 | ✅ |
| AC-IN-03 | E-IN | `grid_g1`, [0][0]=7 (중복) | `check_grid_input` | `E005` | U-IN-03 | ✅ |

### Track C — Control (`tests/control/`)

| AC ID | Epic | Given | When | Then | TC | 상태 |
|-------|------|-------|------|------|-----|------|
| AC-FLOW-01 | E-FLOW | `grid_g1` (입력 유효) | `analyze_grid` | `error=None`, `blank_coords=[(2,3),(4,4)]`, `validation.incomplete` | C-FLOW-01 | ✅ |
| AC-FLOW-02 | E-FLOW | `grid=None` | `analyze_grid` | `error=E003`, `blank_coords=[]`, `validation={}` | C-FLOW-02 | ✅ |

### Golden Master

| AC ID | Epic | Given | Then | TC | 상태 |
|-------|------|-------|------|-----|------|
| AC-GM-01 | E-GM | D-LOC-01 PASS | golden ↔ `find_blank_coords` 출력 일치 | GM-D-LOC-01 | ✅ |
| AC-GM-02 | E-GM | T2 PASS | golden ↔ `validate_lines` fail 출력 일치 | GM-T2 | ✅ |

### AC 판정 우선순위 (`check_grid_input`)

```
1. grid is None        → E003
2. cell ∉ {0, 1~16}    → E004
3. duplicate in 1~16   → E005
4. otherwise           → None
```

### AC 판정 우선순위 (`validate_lines`)

```
1. 빈칸(0) 존재        → incomplete
2. 16칸 채움 + 10선    → pass | fail + failed_lines
```

---

## C2C 추적표 (PRD → To-Do → TC)

| Epic | To-Do | TC ID | Report |
|------|-------|-------|--------|
| E-VAL | fail + failed_lines | T2 | [001](Report/001-arrr-t2-validate-lines.md) |
| E-VAL | incomplete | T1 | [002](Report/002-arrr-t1-validate-lines.md) |
| E-VAL | pass | T3 | [003](Report/003-arrr-t3-validate-lines.md) |
| E-IN | None → E003 | U-IN-01 | [004](Report/004-arrr-u-in-01-boundary.md) |
| E-IN | 범위 밖 → E004 | U-IN-02 | [005](Report/005-arrr-u-in-02-boundary.md) |
| E-LOC | 빈칸 좌표 | D-LOC-01 | [006](Report/006-arrr-d-loc-01-entity.md) |
| E-FLOW · E-GM · E-IN · E-HINT | test-plan 1~4 | C-FLOW-01, GM, U-IN-03, D-HINT-01 | [007](Report/007-arrr-test-plan-backlog.md) |
| E-FLOW | None → E003 (Control) | C-FLOW-02 | [008](Report/008-arrr-c-flow-02-control.md) |
| E-GM | T2 golden | GM-T2 | [009](Report/009-arrr-gm-t2-golden.md) |

---

## Fixture SSOT (`tests/conftest.py`)

| Fixture | 용도 | AC |
|---------|------|-----|
| `grid_g1` | 빈칸 2개 — (2,3), (4,4) | T1, D-LOC-01, U-IN-02/03, C-FLOW-01, D-HINT-01 |
| `grid_complete` | G1 빈칸 채움 | T2 |
| `grid_valid_magic` | 유효 마방진 (10선=34) | T3 |

---

## 백로그 (다음 AC)

| 후보 | Epic | 필요성 |
|------|------|--------|
| golden U-IN-01 | E-GM | 회귀 확장 |
| 격자 크기 검증 | E-IN | 4×4 아닌 입력 |
| 힌트 2번째 빈칸 | E-HINT | 빈칸 1개 남을 때 |

---

## 검증 현황

```powershell
pytest tests/ -v
# → 10 passed
```

| Track | TC |
|-------|-----|
| Entity | T1, T2, T3, D-LOC-01, D-HINT-01 |
| Boundary | U-IN-01, U-IN-02, U-IN-03 |
| Control | C-FLOW-01, C-FLOW-02 |

---

## 관련 문서

- [README](../README.md)
- [테스트 플랜](test-plan.md)
- [학습 가이드](learning-guide.md)
- [`.cursorrules`](../.cursorrules)
- ARRR Report: [`docs/Report/`](Report/)
