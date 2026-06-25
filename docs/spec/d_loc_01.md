# spec 산출물 — `find_blank_coords` (D-LOC-01)

| 항목 | 내용 |
|------|------|
| **브랜치** | `spec` |
| **Track** | B — Entity (Logic) |
| **TC ID** | D-LOC-01 |

---

## 1. PRD · To-Do

| PRD | To-Do | TC |
|-----|-------|-----|
| 빈칸에 유효 숫자 입력 (선행) | 빈칸(0) **두 곳** 좌표 찾기 | **D-LOC-01** |

부분 마방진에서 **어디를 채워야 하는지** 알려 주는 Entity 기능.

---

## 2. R-G-I-O

| | 내용 |
|---|------|
| **R** Role | ECB Entity — 순수 도메인. Boundary/Control import 금지. |
| **G** Goal | 4×4 격자에서 `BLANK_CELL`(0)인 칸의 **1-index 좌표** 목록을 row-major 순으로 반환 |
| **I** Input | `grid: list[list[int]]` — 4×4 |
| **O** Output | `list[tuple[int, int]]` — `(row, col)` 1-index, row-major |

---

## 3. 함수 계약

| 항목 | 값 |
|------|-----|
| 모듈 | `src/entity/find_blank_coords.py` |
| SSOT | `BLANK_CELL`, `GRID_SIZE` — `src/entity/constants.py` |

### 좌표 규칙 (I6)

- **1-index:** 행·열 모두 1부터 시작
- **row-major:** 행 우선 스캔 (R1→R4, 각 행 C1→C4)

### G1 fixture 기대값

| 격자 | 빈칸 1-index |
|------|--------------|
| `grid_g1` | `(2, 3)`, `(4, 4)` |

```
16   2   3  13     ← R1
 5  11   0   8     ← R2, C3 = 0
 9   7   6  12
 4  14  15   0     ← R4, C4 = 0
```

**Then:** `find_blank_coords(grid_g1) == [(2, 3), (4, 4)]`

---

## 4. C2C · RED

| TC ID | Given | Then |
|-------|-------|------|
| **D-LOC-01** | `grid_g1` | `[(2, 3), (4, 4)]` |

**다음 RED:** D-LOC-01

---

## 5. ECB

```
Boundary  check_grid_input (U-IN-01/02)
Control   (향후) find_blank_coords → validate_lines 조합
Entity    find_blank_coords(grid)  ← 본 spec
```
