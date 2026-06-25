# spec — U-IN-03: 중복 숫자 → E005

| 항목 | 내용 |
|------|------|
| **TC ID** | U-IN-03 |
| **Epic** | E-IN |
| **함수** | `check_grid_input` 확장 |

## 판정 순서

1. `grid is None` → E003
2. cell out of range → E004
3. duplicate in 1~16 → **E005**
4. otherwise → None

## AC

- **Given:** `grid_g1`, `[0][0]`과 `[2][1]` 모두 `7`
- **Then:** `check_grid_input(grid) == E005`
