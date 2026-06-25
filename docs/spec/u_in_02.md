# spec 산출물 — `check_grid_input` 범위 검증 (U-IN-02)

| 항목 | 내용 |
|------|------|
| **브랜치** | `spec` |
| **Track** | A — Boundary |
| **TC ID** | U-IN-02 |
| **선행** | U-IN-01 (`E003`) |

---

## 1. PRD · To-Do

| PRD | To-Do | TC |
|-----|-------|-----|
| 1~16 범위 밖 숫자 입력 방지 | 유효 범위 밖 셀 → **E004** | **U-IN-02** |

**유효 셀 값:** `BLANK_CELL`(0) 또는 `1` ~ `GRID_SIZE²`(16)

Mom Test 확장 질문: 「0이나 17 같은 값을 넣었을 때, 그걸 언제 어떻게 알았나요?」

---

## 2. R-G-I-O (U-IN-02 추가 계약)

| | 내용 |
|---|------|
| **R** Role | ECB Boundary — U-IN-01에 이어 입력 범위 검증 |
| **G** Goal | 격자 셀 값이 `0`·`1~16` 밖이면 **E004** 반환 |
| **I** Input | `grid: list[list[int]]` (None 아님 — U-IN-01 선행) |
| **O** Output | `E004` 또는 `None` |

### `check_grid_input` 판정 순서 (갱신)

```
1. grid is None        → E003
2. any cell out of range → E004
3. otherwise           → None
```

**유효 범위:** `BLANK_CELL` 또는 `1 <= value <= GRID_SIZE * GRID_SIZE`  
SSOT: `src/entity/constants.py`의 `BLANK_CELL`, `GRID_SIZE`

---

## 3. 에러 코드

| 코드 | 의미 |
|------|------|
| `E004` | 셀 값이 유효 범위(0, 1~16) 밖 |

---

## 4. C2C · RED

| TC ID | Given | Then |
|-------|-------|------|
| **U-IN-02** | `grid_g1`에서 한 칸을 `17`로 변경 | `check_grid_input(grid) == E004` |

**다음 RED:** U-IN-02
