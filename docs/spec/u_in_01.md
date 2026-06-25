# spec 산출물 — `check_grid_input` (U-IN-01)

| 항목 | 내용 |
|------|------|
| **브랜치** | `spec` |
| **단계** | ② 설계 |
| **레이어** | Boundary (`src/boundary/`) |
| **Track** | A — UI/Boundary |
| **TC ID** | U-IN-01 |

---

## 1. PRD · To-Do

| PRD | To-Do | TC |
|-----|-------|-----|
| grid=None 처리 | None 입력 시 **E003** 반환 | **U-IN-01** |

Entity `validate_lines` 호출 **전** Boundary에서 입력 유효성을 검사한다.

---

## 2. R-G-I-O

| | 내용 |
|---|------|
| **R** Role | ECB Boundary — 입출력·에러 코드 담당. Entity 로직을 직접 구현하지 않음. |
| **G** Goal | 격자 입력이 `None`일 때 **E003** 에러 코드를 반환해 후속 처리를 중단한다. |
| **I** Input | `grid: list[list[int]] \| None` |
| **O** Output | `str \| None` — 오류 시 에러 코드(`E003`), 유효 시 `None` |

---

## 3. 함수 계약 — `check_grid_input`

| 항목 | 값 |
|------|-----|
| 모듈 | `src/boundary/grid_input.py` (GREEN에서 생성) |
| import | `src/boundary/error_codes.py`의 `E003` SSOT |

### 판정

| 조건 | 반환 |
|------|------|
| `grid is None` | `E003` |
| 그 외 (본 TC 범위) | `None` |

> U-IN-02 이후: 범위 밖 숫자 등 추가 입력 검증 확장.

---

## 4. 에러 코드 SSOT

| 코드 | 의미 | 모듈 |
|------|------|------|
| `E003` | 격자 입력이 None | `src/boundary/error_codes.py` |

---

## 5. C2C · RED

| TC ID | Given | Then | 테스트 경로 |
|-------|-------|------|-------------|
| **U-IN-01** | `grid=None` | `check_grid_input(None) == E003` | `tests/boundary/` |

**다음 RED:** U-IN-01

---

## 6. ECB 배치

```
Boundary  check_grid_input(None) → E003
    ↓ (None이 아닐 때만)
Control   (향후) Entity 조합
    ↓
Entity    validate_lines(grid)
```

Entity는 Boundary/Control을 **import하지 않음**.
