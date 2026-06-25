# spec — D-HINT-01: 힌트 1칸

| 항목 | 내용 |
|------|------|
| **TC ID** | D-HINT-01 |
| **Epic** | E-HINT |
| **함수** | `hint_one_cell(grid)` — `src/entity/` |

## AC

- **Given:** `grid_g1` (빈칸 2개)
- **When:** `hint_one_cell(grid_g1)`
- **Then:** `(2, 3)` — row-major 첫 빈칸 (1-index)
