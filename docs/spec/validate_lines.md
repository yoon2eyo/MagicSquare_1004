# spec 산출물 — `validate_lines` 설계 계약

| 항목 | 내용 |
|------|------|
| **브랜치** | `spec` |
| **단계** | ② 설계 |
| **레이어** | Entity (`src/entity/`) |
| **상태** | 확정 — RED(T2) 착수 가능 |

> 코드 구현·테스트 assert는 **하지 않는다.** 본 문서가 `spec` 단계 SSOT이다.  
> 구현 SSOT는 `.cursorrules` + 본 문서 + `src/entity/constants.py`.

---

## 1. Mom Test — 진짜 문제 (① 산출물)

> **진짜 문제:** 부분 마방진을 채우는 동안 10개 줄의 합(34)을 즉시 판정하고, 틀린 줄을 바로 알 수 없어 확인에 시간이 낭비된다.

### Mom Test에서 확인된 사실

| 회차 | 사실 |
|------|------|
| 1 | 행 4개 합만 확인하고 대각선을 빼먹어 **20분 추가** 소요 |
| 2 | 검증 순서: 행 → 열 → 대각선 (**10선을 한 번에 보지 않음**) |
| 3 | 줄 ID 없이 연필 **밑줄**로만 표시 (R2, D1 등 이름 없음) |
| 4 | 빈칸 때문에 합 ≠ 34일 때 **틀림 vs 미완성** 구분 불가 |

---

## 2. Mom Test → 설계 매핑

| Mom Test 사실 | 설계 반영 | 계약 항목 |
|---------------|-----------|-----------|
| 대각선을 빼먹음 | 10선 전체 검증 | R1~R4, C1~C4, **D1, D2** |
| 틀린 줄을 바로 못 말함 | 실패 줄 ID 반환 | `fail` + **`failed_lines`** |
| 빈칸 vs 틀림 구분 불가 | 상태 3분할 | **`incomplete`** vs **`fail`** |
| 부분 검증으로 시간 낭비 | 한 함수 호출로 10선 즉시 판정 | `validate_lines(grid)` |

### `incomplete` vs `fail` — Mom Test 연결 (필수)

**연결 사실 (4회차):**  
「빈칸 때문에 합이 34가 안 나와서, 틀린 건지 아직 안 채운 건지 구분이 안 됐다.」

| status | 학습자에게 의미 | 설계 이유 |
|--------|----------------|-----------|
| `incomplete` | 아직 완성 전 — **오류 아님** | 빈칸(`BLANK_CELL`)이 있으면 합 ≠ 34여도 `fail`로 판정하지 않음 |
| `fail` | 16칸을 다 채웠는데 틀림 — **어느 줄인지 표시** | `failed_lines`로 R/C/D ID 즉시 제공 |

`failed_lines`는 **`fail`일 때만** 반환한다. `incomplete`에서 줄 ID를 내리면, 아직 채우지 않은 줄까지 「틀렸다」고 오해할 수 있다 (Mom Test 3회차).

---

## 3. R-G-I-O

| | 내용 |
|---|------|
| **R** Role | TDD·ECB를 지키는 시니어 개발자. Entity에 **순수 도메인 로직**만 두고, Boundary/Control import 금지. |
| **G** Goal | 4×4 격자에 대해 **10선 합을 즉시 판정**하고, 틀렸을 때 **실패 줄 ID(`failed_lines`)** 를 반환한다. Mom Test 진짜 문제를 한 함수 계약으로 흡수한다. |
| **I** Input | `grid: list[list[int]]` — 4×4 격자. 각 칸: `BLANK_CELL`(0) = 빈칸, `1`~`16` = 채워진 숫자. |
| **O** Output | `{ "status": str, "failed_lines": list[str] \| None }` — `status`는 `pass` \| `fail` \| `incomplete`. `failed_lines`는 `fail`일 때만 비어 있지 않은 목록. |

---

## 4. 함수 계약 — `validate_lines`

### 4.1 배치

| 항목 | 값 |
|------|-----|
| 모듈 | `src/entity/validate_lines.py` (GREEN 단계에서 생성) |
| 레이어 | Entity |
| import 금지 | `src/boundary/`, `src/control/` |

### 4.2 시그니처 (설계)

```python
def validate_lines(grid: list[list[int]]) -> dict[str, object]:
    ...
```

### 4.3 판정 우선순위

```
1. 격자에 BLANK_CELL(0)이 하나라도 있음 → incomplete  (10선 합 검사 생략)
2. 16칸 모두 채워짐 → 10선 각각 MAGIC_CONSTANT(34)와 비교
   2a. 모두 34 → pass
   2b. 하나라도 ≠ 34 → fail + failed_lines (합 ≠ 34인 줄 ID 전부)
```

### 4.4 status 계약

| status | 조건 | `failed_lines` |
|--------|------|----------------|
| `incomplete` | 격자에 `BLANK_CELL`(0)이 **하나라도** 있음 | `None` 또는 `[]` (테스트에서 `fail`과 구분만 되면 됨) |
| `pass` | 16칸 모두 채워짐 + 10선 합이 **모두** `MAGIC_CONSTANT` | `None` 또는 `[]` |
| `fail` | 16칸 모두 채워짐 + **어느 한 줄이라도** 합 ≠ `MAGIC_CONSTANT` | 해당 줄 ID **전부** (순서: R1→R4, C1→C4, D1, D2) |

### 4.5 10선 정의 (줄 ID)

격자 `grid[r][c]` — `r`, `c`는 **0-index** (0~3). 줄 ID는 **1-index** 이름.

| ID | 의미 | 포함 칸 (0-index) |
|----|------|-------------------|
| `R1`~`R4` | 행 | `grid[i][0..3]` — `Ri` = `grid[i-1]` |
| `C1`~`C4` | 열 | `grid[0..3][j]` — `Cj` = `grid[..][j-1]` |
| `D1` | 주대각선 ↘ | `(0,0), (1,1), (2,2), (3,3)` |
| `D2` | 부대각선 ↙ | `(0,3), (1,2), (2,1), (3,0)` |

### 4.6 상수 SSOT

| 상수 | 값 | 정의 위치 |
|------|-----|-----------|
| `MAGIC_CONSTANT` | 34 | `src/entity/constants.py` |
| `BLANK_CELL` | 0 | `src/entity/constants.py` |
| `GRID_SIZE` | 4 | `src/entity/constants.py` |

리터럴 `34`, `0` 하드코딩 **금지**.

---

## 5. C2C — PRD → To-Do → Test Case

### 5.1 PRD (기능 요구)

| ID | 요구 | Mom Test 근거 |
|----|------|---------------|
| FR-VAL-01 | 10선 합 34 즉시 판정 | 1·2회차 — 부분 검증·시간 낭비 |
| FR-VAL-02 | 실패 줄 ID 표시 | 3회차 — 줄 이름 없이 밑줄만 |
| FR-VAL-03 | 미완성 vs 오류 구분 | 4회차 — 빈칸 vs 틀림 혼동 |

### 5.2 To-Do → TC (1 To-Do : 1 TC)

| To-Do | TC ID | Given | Then | RED 우선순위 |
|-------|-------|-------|------|--------------|
| 빈칸 있으면 incomplete | **T1** | `grid_g1` (빈칸 2개) | `status == "incomplete"` | 2 |
| 완성 격자에서 한 칸 틀리면 fail + 줄 ID | **T2** | `grid_complete`, 1-index (2,2) 값 11→12 | `status == "fail"`, `"R2"`, `"C2"` ∈ `failed_lines` | **1 (다음 RED)** |
| 완성·올바른 마방진이면 pass | **T3** | 완성 유효 마방진 | `status == "pass"`, `failed_lines` 비어 있음 | 3 |

> **다음 RED:** `T2` — `fail` + `failed_lines`가 Mom Test 진짜 문제의 핵심이다.

### 5.3 T2 fixture 메모 (RED 준비용)

완성 격자 `grid_complete` (G1 빈칸 채움 — conftest에 RED 전 추가):

```
16   2   3  13
 5  11  10   8
 9   7   6  12
 4  14  15   1
```

| 항목 | 값 |
|------|-----|
| **Given** | `grid_complete`에서 **1-index (2,2)** = 0-index `[1][1]` 값 `11` → `12` 변경 |
| **Then** | `status == "fail"`, `"R2"`, `"C2"` ∈ `failed_lines` |

---

## 6. 범위 · 비범위

### 포함 (본 spec)

- `validate_lines` 단일 함수 계약
- 3 status + `failed_lines`
- Entity 레이어 배치

### 제외 (별 spec / 별 ARRR)

- `find_blank_coords` (D-LOC-01) — 별 To-Do
- Boundary 입력 검증 (`grid=None` → E003)
- UI 표시·색칠
- 1~16 중복·범위 검증 (확장 ⑦)

---

## 7. spec 완료 기준 · 다음 단계

### 완료 기준 (체크)

- [x] 진짜 문제 한 문장 확정
- [x] R-G-I-O 4칸 작성
- [x] `validate_lines` status 계약 + 판정 우선순위
- [x] 10선 ID 정의
- [x] Mom Test 사실 ↔ 설계 매핑
- [x] C2C: PRD → To-Do → TC (T1~T3)
- [x] 다음 RED 후보: **T2**

### 다음 단계

```powershell
git checkout red
# /red-skeleton — Test ID: T2
pytest tests/ -v   # → FAILED 확인
```

---

## 관련 문서

- [학습 가이드 — ② 설계](../learning-guide.md#②-설계--r-g-i-o--validate_lines-계약)
- [`.cursorrules`](../../.cursorrules)
- [AGENTS.md](../../AGENTS.md)
