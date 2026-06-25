# C2C · Dual-Track · ARRR — 개념 학습

> **대상:** MagicSquare_1004 실습 전·중에 “왜 이렇게 하는가?”를 한 번에 정리하고 싶은 학습자  
> **연결 문서:** [`PRD.md`](PRD.md) · [`learning-guide.md`](learning-guide.md) · [`test-plan.md`](test-plan.md)

---

## 한 줄 요약

**C2C(Concept-to-Code Traceability)** = 요구·개념이 코드까지 **추적 가능**해야 한다.  
그 추적성을 **확보하는 수단**이 **Dual-Track TDD**이고, 그것을 **돌리는 사이클**이 **ARRR**이다.  
세 개는 **따로가 아니다**.

---

## ① 목표 — C2C (개념 → 코드 추적성)

### C2C란?

**Concept-to-Code Traceability** — “왜 이 코드가 존재하는가?”를 **문서 → 테스트 → 구현** 한 줄로 따라갈 수 있는 상태.

```
PRD(요구) → To-Do(할 일) → Test Case(검증) → src/(구현)
     ↑__________________________________________|
                    (역추적 가능)
```

| 질문 | C2C가 있으면 | C2C가 없으면 |
|------|--------------|--------------|
| 이 테스트는 왜 있나? | PRD Epic · Mom Test 사실로 답함 | “예전에 누가 만든 것 같음” |
| 이 버그는 어디서 왔나? | 깨진 TC → To-Do → PRD 한 줄 | “어디가 왜 깨졌는지” 모름 |
| 이 기능 빼도 되나? | PRD에 없으면 코드도 없어야 함 | 죽은 코드·幽霊 테스트 |

**목표는 단 하나:** 요구·개념이 코드까지 추적 가능해야 한다. **이것이 전부의 이유다.**

---

## ② 왜 — 추적성(Traceability)이 필요한가?

### 유래 — C2C는 어디서 왔나?

소프트웨어 공학에서 **요구사항 추적(Requirements Traceability)** 은 오래된 주제다.

- 방위·항공·의료처럼 **감사·규제**가 있는 분야에서는 “요구 ID ↔ 설계 ↔ 테스트 ↔ 코드” 매핑이 **필수**였다.
- 애자일·TDD 이후에는 문서만이 아니라 **실행 가능한 테스트**가 추적의 **고리(hook)** 가 되었다.
- **C2C**는 이 전통을 **개념(Concept)** 과 **코드(Code)** 사이에 **테스트**를 끼워 넣은, 이 프로젝트의 **실습용 이름**이다.

즉, C2C는 “새로운 마법”이 아니라 **“요구가 코드까지 끊기지 않게 잇는 습관”** 에 가깝다.

### 왜 필요한가?

**테스트 없는 코드**는 동작할 수는 있지만, 깨졌을 때 **어디가 왜 깨졌는지** 알 수 없다.

| 상황 | 추적성 없음 | 추적성 있음 (C2C) |
|------|-------------|-------------------|
| `pytest` 1개 FAIL | “뭔가 고쳐야 함” | `T2` FAIL → “행 합 ≠ 34일 때 fail + failed_lines” 계약 위반 |
| 리팩터링 후 회귀 | 전체를 다시 손으로 확인 | 해당 TC만 RED → 원인 좁힘 |
| 요구 변경 | 어디를 고칠지 감 | PRD 한 줄 → To-Do 1개 → TC 1개 → 파일 1개 |

**추적성이 “어디가 왜 깨졌는지” 문제를 푼다.**  
그래서 이 프로젝트는 **판단 항목만** PRD에서 테스트·코드로 **내려보낸다** (C2C 3원칙).

### C2C 3원칙 (`.cursorrules` · `PRD.md`)

1. **판단 항목만 변환** — PRD → To-Do → TC (부가 설명·UI 장식은 제외)
2. **1 To-Do : 1 Test Case** — 한 RED에 여러 ID 동시 해결 금지
3. **RED 먼저** — 구현 전에 의도적 실패로 “이 요구를 검증한다”를 고정

---

## ③ 수단이자 사이클 — Dual-Track TDD = ARRR

### Dual-Track이란?

**Dual-Track** = ECB 아키텍처에 맞춰 **테스트를 두 갈래(Track)** 로 나누는 방식.

| Track | 레이어 | 역할 | 테스트 경로 |
|-------|--------|------|-------------|
| **B — Logic** | Entity (`src/entity/`) | 순수 도메인 (10선 합, 빈칸 좌표 등) | `tests/entity/` |
| **A — UI/Boundary** | Boundary (`src/boundary/`) | 입출력·에러 코드 (None, 범위 밖 등) | `tests/boundary/` |

Control (`src/control/`)은 Entity를 **조합**하는 Track이며, `tests/control/`에서 검증한다.

```
                    ┌── Track B: tests/entity/  (도메인 판단)
  PRD ── To-Do ── TC ─┤
                    └── Track A: tests/boundary/ (입력·에러)
                              tests/control/     (흐름 조합)
```

**왜 “Dual”인가?**

- **같은 PRD**라도 **판단 주체**가 다르다.  
  - “행 합이 34인가?” → Entity (Track B)  
  - “grid가 None이면?” → Boundary (Track A)
- 한 파일에 섞으면 **어디서 깨졌는지** 추적이 흐려진다.
- Track을 나누면 **C2C 한 줄**이 **폴더·레이어**까지 이어진다.

**규칙:** Entity는 Boundary/Control를 **import하지 않는다** — 도메인만 테스트·구현한다.

### Dual-Track TDD를 돌리는 것 = ARRR

**Dual-Track TDD**를 **Ask · Respond · Refine · Repeat**로 돌리는 것이 곧 **추적성 확보**다. **둘은 같다.**

| ARRR | TDD | 브랜치 | 할 일 | C2C에서의 의미 |
|------|-----|--------|-------|----------------|
| **A** — Ask | RED | `red` | 테스트만 · `src/` 수정 금지 · `pytest.fail` | “이 To-Do를 **이 TC**로 검증한다” 고정 |
| **R** — Respond | GREEN | `green` | 최소 구현 · 1 RED = 1 커밋 | PRD 한 줄이 **코드**로 내려옴 |
| **R** — Refine | REFACTOR | `green` | 계약 불변 리팩터 | 구조만 정리 · **추적 고리 유지** |
| **R** — Repeat | 다음 RED | `green` → `red` | `/export` 보고 · 다음 TC 1개 | PRD 표의 **다음 행**으로 이동 |

```
     ┌─────────────────────────────────────────┐
     │  ① 목표: C2C — 개념→코드 추적성          │
     └──────────────────┬──────────────────────┘
                        ▼
     ┌─────────────────────────────────────────┐
     │  ② 왜: 테스트 없으면 “왜 깨졌는지” 모름   │
     └──────────────────┬──────────────────────┘
                        ▼
     ┌─────────────────────────────────────────┐
     │  ③ 수단: Dual-Track TDD = ARRR 사이클    │
     │     Track B/A + RED→GREEN→REFACTOR      │
     └──────────────────┬──────────────────────┘
                        ▼
     ┌─────────────────────────────────────────┐
     │  ④ 결과: 테스트가 지키는 Clean Code      │
     └─────────────────────────────────────────┘
```

---

## ④ 결과 — TDD · 리팩토링으로 Clean Code

C2C + Dual-Track + ARRR을 끝까지 돌리면 얻는 것:

| 결과 | 설명 |
|------|------|
| **추적 가능** | PRD Epic → TC ID → 테스트 파일 → `src/` 모듈 |
| **테스트가 보호** | REFACTOR해도 계약( assert )이 깨지면 즉시 RED |
| **계속 손볼 수 있음** | “왜 있는 코드인지” 알기 때문에 과감히 정리 가능 |

이 프로젝트의 **Clean Code**는 미학이 아니라 **계약 불변 + 전 테스트 PASS**다.

---

## 강사 한 마디 — 오해 금지

> **"ARRR"과 "C2C × Dual-Track TDD"는 따로가 아닙니다.**  
> ARRR(질문→응답→정제→반복)을 돌리는 것이 곧 Dual-Track TDD 실행이고,  
> 그것이 C2C(추적성)를 **담보**하는 방법입니다.

**머릿속에 새길 한 줄:**

```
Ask = RED  |  Respond = GREEN  |  Refine = REFACTOR  |  Repeat = 다음 질문
```

오늘 실습의 성공 기준: 위 한 줄로 **다음에 뭘 할지** (어느 Track, 어느 TC ID) 바로 말할 수 있으면 된다.

---

## MagicSquare에서의 C2C × Dual-Track 예시

### Track B (Logic) — `D-LOC-01`

| 단계 | 내용 |
|------|------|
| PRD | 빈칸(0) 두 곳 좌표를 찾는다 |
| To-Do | `find_blank_coords` — 1-index, row-major |
| TC ID | `D-LOC-01` |
| 테스트 | `tests/entity/test_d_loc_01_blank_coords_row_major.py` |
| 구현 | `src/entity/find_blank_coords.py` |
| Report | [`Report/006`](Report/006-arrr-d-loc-01-entity.md) |

### Track A (Boundary) — `U-IN-01`

| 단계 | 내용 |
|------|------|
| PRD | grid=None 처리 |
| To-Do | None → 에러 코드 E003 |
| TC ID | `U-IN-01` |
| 테스트 | `tests/boundary/test_u_in_01_none_grid_returns_e003.py` |
| 구현 | `src/boundary/grid_input.py` |
| Report | [`Report/004`](Report/004-arrr-u-in-01-boundary.md) |

**같은 Mom Test(“확인에 시간 낭비”)** 에서 나온 요구도, **판단 주체**에 따라 Track과 TC가 갈린다.

전체 추적표: [`PRD.md` § C2C 추적표](PRD.md#c2c-추적표-prd--to-do--tc)

---

## 자가 점검 (3문항)

1. **C2C:** 지금 보고 있는 테스트 파일 이름만 보고, PRD의 **어느 Epic·To-Do**인지 말할 수 있는가?
2. **Dual-Track:** 그 TC가 `tests/entity/`인지 `tests/boundary/`인지, **왜 그 Track**인지 설명할 수 있는가?
3. **ARRR:** 지금 브랜치가 `red`인지 `green`인지, **Ask/Respond/Refine/Repeat 중 어디**인지 말할 수 있는가?

세 가지 모두 “예”면 개념 정리는 끝이다. 다음은 [`learning-guide.md`](learning-guide.md) ③ Ask(RED)부터 실습하면 된다.

---

## 용어 색인

| 용어 | 의미 |
|------|------|
| **C2C** | Concept-to-Code Traceability — 개념→코드 추적성 |
| **Traceability** | 요구·테스트·코드 간 양방향 연결 |
| **Dual-Track** | ECB에 맞춘 Logic(B) / Boundary(A) 테스트 분리 |
| **ARRR** | Ask · Respond · Refine · Repeat — TDD 사이클의 학습용 이름 |
| **ECB** | Entity · Control · Boundary — 레이어 구조 |
| **RED / GREEN / REFACTOR** | TDD 3단계 (ARRR의 A / R / R에 대응) |
