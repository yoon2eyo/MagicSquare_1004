# MagicSquare_1004

4×4 마방진 자동 검증 — TDD · ECB · ARRR 학습 프로젝트

> 요구·수용 기준 SSOT: [`docs/PRD.md`](docs/PRD.md)  
> 실습 절차: [`docs/learning-guide.md`](docs/learning-guide.md)  
> 테스트 플랜: [`docs/test-plan.md`](docs/test-plan.md)

```powershell
pip install -e ".[dev]"
pytest tests/ -v
# → 12 passed
```

---

## 완료 현황 (GREEN)

| TC ID | Epic | Track | 레이어 | 테스트 |
|-------|------|-------|--------|--------|
| T2 | E-VAL | B | Entity | `tests/entity/test_t2_row_sum_not_34_is_fail.py` |
| T1 | E-VAL | B | Entity | `tests/entity/test_t1_blank_grid_is_incomplete.py` |
| T3 | E-VAL | B | Entity | `tests/entity/test_t3_valid_magic_square_is_pass.py` |
| D-LOC-01 | E-LOC | B | Entity | `tests/entity/test_d_loc_01_blank_coords_row_major.py` |
| D-HINT-01 | E-HINT | B | Entity | `tests/entity/test_d_hint_01_single_hint_coord.py` |
| D-HINT-02 | E-HINT | B | Entity | `tests/entity/test_d_hint_02_one_blank_hint_coord.py` |
| U-IN-01 | E-IN | A | Boundary | `tests/boundary/test_u_in_01_none_grid_returns_e003.py` |
| U-IN-02 | E-IN | A | Boundary | `tests/boundary/test_u_in_02_out_of_range_cell_returns_e004.py` |
| U-IN-03 | E-IN | A | Boundary | `tests/boundary/test_u_in_03_duplicate_cell_returns_e005.py` |
| U-IN-04 | E-IN | A | Boundary | `tests/boundary/test_u_in_04_wrong_grid_size_returns_e006.py` |
| C-FLOW-01 | E-FLOW | C | Control | `tests/control/test_c_flow_01_partial_grid_analysis.py` |
| C-FLOW-02 | E-FLOW | C | Control | `tests/control/test_c_flow_02_none_grid_returns_e003.py` |

**Golden Master:** D-LOC-01 · T2 · U-IN-01 — `tests/golden/` · [`Report/010`](docs/Report/010-arrr-gm-u-in-01-golden.md)

현재: **`pytest tests/ -v` → 12 passed**

### ECB 구현 맵

| 레이어 | 모듈 |
|--------|------|
| Entity | `validate_lines`, `find_blank_coords`, `hint_one_cell` |
| Boundary | `check_grid_input`, `error_codes` (E003~E006) |
| Control | `analyze_grid` |

---

## 다음 백로그 (RED 후보)

| 우선순위 | Epic | TC (안) | To-Do |
|----------|------|---------|-------|
| 1 | — | — | `green` → `main` merge |

브랜치: `spec` → `red` → `green` · 규칙: [`.cursorrules`](.cursorrules)

---

## ARRR · 브랜치

```
spec → red (RED) → green (GREEN → REFACTOR → export) → main
```

| 단계 | 브랜치 | 산출 |
|------|--------|------|
| ② 설계 | `spec` | `docs/spec/*.md` |
| ③ Ask | `red` | `tests/**` + `pytest.fail` |
| ④ Respond | `green` | `src/**` + `assert` |
| ⑤ Refine | `green` | 계약 불변 리팩터 |
| ⑥ Repeat | `green` | `docs/Report/` |

### RED 공통 체크리스트

- [ ] `spec` — R-G-I-O · 계약 문서
- [ ] `red` — Given/When/Then + `pytest.fail` 1줄 · `src/` 수정 금지
- [ ] `green` — 최소 구현 · 1 RED = 1 커밋 · 전체 PASS

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [`docs/PRD.md`](docs/PRD.md) | INV · E · AC |
| [`docs/test-plan.md`](docs/test-plan.md) | test-plan 백로그 (1~4 완료) |
| [`docs/c2c-dual-track-concepts.md`](docs/c2c-dual-track-concepts.md) | C2C · Dual-Track · ARRR |
| [`docs/learning-guide.md`](docs/learning-guide.md) | Mom Test · 브랜치별 절차 |
| [`docs/Report/`](docs/Report/) | ARRR 사이클 보고 (001~013) · **main merge** |
| [`AGENTS.md`](AGENTS.md) | 실행 · ECB 구조 |
