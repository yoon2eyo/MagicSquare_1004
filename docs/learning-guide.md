# 마방진 구현 학습 가이드

4×4 마방진을 **만드는 과정**을 통해 TDD·ECB·ARRR을 체득하는 실습 문서입니다.  
각 단계마다 **브랜치**, **슬래시 명령**, **프롬프트 입력 예**를 함께 적었습니다.

---

## 전체 7단계 한눈에

| 단계 | 이름 | 브랜치 | 핵심 산출물 |
|------|------|--------|-------------|
| ① | 주제 발견 | (전 과정 Ask) | Mom Test로 확인한 **진짜 문제** 한 문장 |
| ② | 설계 | `spec` | R-G-I-O + `validate_lines` 계약 |
| ③ | Ask (RED) | `red` | 의도적으로 실패하는 테스트 |
| ④ | Respond (GREEN) | `green` | 최소 구현 + Golden Master |
| ⑤ | Refine (REFACTOR) | `green` | 계약 불변 리팩터링 |
| ⑥ | Repeat | `green` | `/export` 보고 + 다음 RED 후보 |
| ⑦ | 확장 | `green` → 새 ARRR | 새 기능 = 새 ARRR 사이클 |

브랜치 흐름: `main` → `staging` → `spec` → `red` → `green`

> **병합 방향:** 기능이 완성되면 `green` → `main`(또는 `staging`)으로 합칩니다.  
> **개발 흐름:** 새 기능마다 `spec` → `red` → `green`을 반복합니다.

---

## 브랜치별 작업 과정

각 브랜치에서 **무엇을 하고, 무엇을 하면 안 되는지**, **산출물**과 **완료 기준**을 정리했습니다.

### 한눈에 — 브랜치 × 단계

| 브랜치 | ARRR 단계 | `src/` 수정 | `tests/` 수정 | 핵심 산출물 |
|--------|-----------|-------------|---------------|-------------|
| `main` | (배포·안정) | ❌ 직접 작업 금지 | ❌ | 검증된 코드만 유지 |
| `staging` | 환경 셋업 | ✅ 골격만 | ✅ 골격·fixture | 프로젝트 뼈대 |
| `spec` | ② 설계 | ❌ | ❌ | R-G-I-O + 계약 문서 |
| `red` | ③ Ask (RED) | ❌ **금지** | ✅ 테스트만 | `pytest` **FAILED** |
| `green` | ④⑤⑥ GREEN·REFACTOR·Repeat | ✅ 최소 구현 | ✅ assert·golden | `pytest` **PASS** + 커밋 |

---

### `main` — 안정 브랜치

**역할:** GitHub에 공개되는 **기준선**. 학습자가 직접 기능을 개발하지 않습니다.

| 항목 | 내용 |
|------|------|
| **언제** | `green`에서 ARRR 1사이클(또는 그 이상)이 끝난 뒤 |
| **할 일** | `green`의 검증된 커밋을 merge · push |
| **하지 말 것** | Mom Test, RED, GREEN을 `main`에서 직접 진행 |
| **산출물** | 전체 테스트 PASS 상태의 저장소 |
| **완료 기준** | `pytest tests/ -v` 전체 PASS · 원격 `origin/main`과 동기화 |

```powershell
git checkout main
git merge green
git push origin main
```

---

### `staging` — 환경·골격 셋업

**역할:** TDD·ECB·ARRR을 돌릴 **프로젝트 뼈대**를 만드는 브랜치. 기능 구현은 여기서 하지 않습니다.

| 항목 | 내용 |
|------|------|
| **언제** | 프로젝트를 처음 시작할 때 **1회** (이미 완료됨) |
| **할 일** | 아래 체크리스트 순서대로 진행 |
| **하지 말 것** | `validate_lines` 등 도메인 로직 구현 · RED 테스트 본문 작성 |
| **산출물** | 실행 가능한 빈 ECB 구조 + 규칙 파일 |
| **완료 기준** | `pip install -e ".[dev]"` · `pytest tests/ -v` 실행 가능(테스트 0개 또는 수집만) |

#### 작업 순서

1. **저장소·브랜치**
   - `git init` · 초기 커밋
   - `staging`, `spec`, `red`, `green` 브랜치 생성
2. **패키지·폴더**
   - `pyproject.toml` — `pip install -e ".[dev]"`
   - `src/entity/`, `src/control/`, `src/boundary/`
   - `tests/entity/`, `tests/boundary/`, `tests/golden/`
3. **SSOT 상수**
   - `src/entity/constants.py` — `MAGIC_CONSTANT`, `BLANK_CELL`, `GRID_SIZE`
4. **공통 fixture**
   - `tests/conftest.py` — `grid_g1` (빈칸 2개 부분 마방진)
5. **규칙·명령**
   - `.cursorrules` — ECB, `validate_lines` 계약, TDD 금지 사항
   - `.cursor/commands/` — `/tdd-red`, `/green-minimal` 등
   - `AGENTS.md`
6. **문서**
   - `docs/github-push-guide.md`
   - `docs/learning-guide.md` (본 문서)
7. **원격 push** (선택)
   - `git push -u origin staging` 및 나머지 브랜치 push

```powershell
git checkout staging
pip install -e ".[dev]"
pytest tests/ -v
```

**현재 상태 (이 프로젝트):** 위 항목은 커밋 `3322c18` 기준으로 **완료**되어 있으며, `staging`·`spec`·`red`·`green`이 동일 커밋을 가리킵니다.

---

### `spec` — 설계 (②)

**역할:** Mom Test **진짜 문제**를 **코드 계약**으로 바꾸는 단계. **코드는 작성하지 않습니다.**

| 항목 | 내용 |
|------|------|
| **언제** | Mom Test로 진짜 문제 한 문장이 확정된 직후 · **RED 전에 반드시** |
| **할 일** | R-G-I-O 표 · 함수 계약 · Mom Test 사실 ↔ 설계 매핑 |
| **하지 말 것** | `src/` 구현 · `tests/`에 assert 본문 · `pytest.fail` 제거 |
| **산출물** | 설계 문서(본 가이드 ②절 또는 `docs/` 보강) |
| **완료 기준** | R-G-I-O 4칸 채움 · `incomplete`/`fail` 구분 이유가 Mom Test 사실 1개와 연결됨 |

#### 작업 순서

1. **브랜치 전환**
   ```powershell
   git checkout spec
   ```
2. **진짜 문제 확인** (① 산출물)
   > **진짜 문제:** 부분 마방진을 채우는 동안 10개 줄의 합(34)을 즉시 판정하고, 틀린 줄을 바로 알 수 없어 확인에 시간이 낭비된다.
3. **R-G-I-O 표 작성** — 대상 함수·모듈 단위 (예: `validate_lines`)
4. **계약 표 작성** — `pass` / `fail` / `incomplete` 조건 · `failed_lines` 줄 ID
5. **Mom Test → 설계 매핑** — 사실 1개당 계약 항목 1개
6. **C2C 설계표** (선택) — PRD → To-Do → TC ID 목록 (아직 테스트 파일은 만들지 않음)
7. **커밋** — 문서만 (`docs/`, `.cursorrules` 보강 등). `src/` 로직 추가 없음
8. **다음 브랜치로** — `git checkout red`

#### `validate_lines` 계약 (SSOT)

| status | 조건 | `failed_lines` |
|--------|------|----------------|
| `incomplete` | 격자에 `0`(빈칸)이 하나라도 있음 | 없음 |
| `pass` | 16칸 모두 채워짐 + 10선 합이 모두 34 | 없음 |
| `fail` | 16칸 모두 채워짐 + 어느 한 줄이라도 합 ≠ 34 | 해당 줄 ID 목록 |

**판정 우선순위:** 빈칸 있음 → `incomplete` (합으로 `fail` 판정하지 않음) → 빈칸 없음 → 10선 검사.

**줄 ID:** `R1`~`R4`, `C1`~`C4`, `D1`, `D2`

#### 프롬프트 입력 예

```
spec 브랜치. validate_lines 계약 검토.
입력: 4×4 격자 (0=빈칸). 출력: pass/fail/incomplete + failed_lines.
Mom Test 진짜 문제: "10선 합 즉시 판정 + 실패 줄 표시".
R-G-I-O 표를 채우고, incomplete와 fail이 구분되는 이유를
Mom Test 사실 1개와 연결해 설명해 주세요. 코드 작성 금지.
```

---

### `red` — Ask / RED (③)

**역할:** 설계 계약을 **실패하는 테스트**로 고정. 구현은 아직 없어야 합니다.

| 항목 | 내용 |
|------|------|
| **언제** | `spec` 계약이 확정된 직후 |
| **할 일** | **1 To-Do : 1 Test Case** — 테스트 파일 + `pytest.fail` 1줄 |
| **하지 말 것** | `src/` **어떤 파일도 수정 금지** · assert로 바꾸기 · skip/xfail |
| **산출물** | `tests/entity/test_*.py` (또는 `tests/boundary/`) |
| **완료 기준** | `pytest tests/ -v` → 해당 TC **FAILED** (의도적 실패) |

#### 작업 순서

1. **브랜치 전환**
   ```powershell
   git checkout red
   ```
2. **C2C 확인** — PRD → To-Do → TC ID 1개만 선택 (예: `T2`, `D-LOC-01`)
3. **설계표** (선택) — `/red-test-plan` — 파일 생성 없이 표만
4. **테스트 skeleton** — `/red-skeleton` 또는 `/tdd-red`
   - Given / When / Then을 주석 또는 docstring으로 명시
   - 본문은 `pytest.fail("RED: …")` **1줄만**
5. **fixture** — 없으면 `tests/conftest.py`에 추가 (격자 데이터만, 로직 없음)
6. **실행 확인**
   ```powershell
   pytest tests/ -v
   # → 1 failed = RED 성공
   # → PASS면 src/에 구현이 남아 있음 → 제거 후 재시도
   ```
7. **커밋** — 테스트 파일만. `src/` diff 없음
8. **다음 브랜치로** — `git checkout green`

#### RED 금지 사항 (`.cursorrules`)

- 한 RED에 여러 TC ID 동시 해결 금지
- `src/` 수정 금지
- `skip`, `xfail` 금지

#### 프롬프트 입력 예 (`validate_lines` T2)

```
/red-skeleton
Test ID: T2 — test_t2_row_sum_not_34_is_fail
Given: 완성 마방진에서 (2,2) 값 6→7 변경
Then: status="fail", failed_lines에 "R2", "C2" 포함
Fixture: 완성 격자 fixture 필요 (conftest에 추가 요청)
src/ 수정 금지.
```

---

### `green` — Respond · Refine · Repeat (④⑤⑥)

**역할:** RED를 통과시키고, 안전하게 정제하고, 문서화한 뒤 다음 RED로 넘어갑니다.  
**REFACTOR(⑤)와 Repeat(⑥)도 `green` 브랜치에서 진행합니다.**

| 항목 | 내용 |
|------|------|
| **언제** | RED가 FAILED로 확인된 직후 |
| **할 일** | 최소 구현 → assert 교체 → Golden Master → (선택) 리팩터 → export |
| **하지 말 것** | GREEN 단계에서 리팩터링 · 한 커밋에 여러 RED 해결 · assert 완화 |
| **산출물** | `src/entity/*.py` 구현 · PASS 테스트 · golden 파일 · 커밋 |
| **완료 기준** | `pytest` PASS · Golden Master 일치 · **1 커밋 = 1 RED** |

#### ④ GREEN — 작업 순서

1. **브랜치 전환**
   ```powershell
   git checkout green
   ```
2. **RED 재확인** — 아직 FAILED인지 `pytest` 실행
3. **최소 구현** — `/green-minimal`
   - RED 1개를 통과시킬 **최소 코드만** `src/`에 추가
   - `MAGIC_CONSTANT`, `BLANK_CELL`은 `constants.py`만 참조 (리터럴 `34`, `0` 금지)
4. **assert 교체** — `pytest.fail` → 실제 `assert`
5. **PASS 확인**
   ```powershell
   pytest tests/ -v
   ```
6. **Golden Master** — `/golden-master`
   ```powershell
   $env:UPDATE_GOLDEN=1; pytest tests/entity/test_xxx.py -v
   pytest tests/entity/test_xxx.py -v
   ```
7. **커밋** — 구현 + 테스트. 메시지에 TC ID 포함 (예: `green: T2 validate_lines fail + failed_lines`)

#### ⑤ REFACTOR — 작업 순서 (전제: 전체 PASS)

1. **냄새 식별** — `/refactor-smell` (코드 수정 없음)
2. **안전 리팩터** — `/refactor-safe`
   - 계약 불변 · ≤3 files · ≤3 methods
3. **회귀 확인** — `pytest` + golden 전부 PASS
4. **커밋** — `refactor: …`

#### ⑥ Repeat — 작업 순서

1. **사이클 보고** — `/export` 또는 `/export-session`
   - 채팅에 있는 pytest 결과만 기재 (없는 결과는 쓰지 않음)
2. **다음 RED 후보 1개** 선정 (C2C 표 갱신)
3. **브랜치 이동** — 다음 기능이면 `git checkout spec`부터, 같은 계약의 다음 TC면 `git checkout red`

```powershell
# ARRR 1사이클 완료 후 안정 브랜치에 반영할 때
git checkout main
git merge green
```

#### 프롬프트 입력 예 (GREEN)

```
/green-minimal
RED 대상: T2
src/entity/validate_lines.py 최소 구현.
MAGIC_CONSTANT·BLANK_CELL은 constants.py SSOT만 사용.
리팩터링 금지. 통과 후 커밋 메시지 초안 제안.
```

---

### 브랜치 전환 — 기능 1개당 전체 흐름

```
① Mom Test (Ask, 브랜치 무관)
        ↓ 진짜 문제 한 문장
② spec    — 설계·계약 문서화
        ↓
③ red     — 테스트만, pytest FAILED
        ↓
④ green   — 최소 구현, pytest PASS, 커밋
        ↓
⑤ green   — refactor (선택)
        ↓
⑥ green   — export, 다음 RED 후보
        ↓
   (다음 TC) → red 반복
   (기능 완료) → main merge
```

```powershell
# 예: validate_lines 첫 TC (T2)
git checkout spec    # 설계 확인·문서 커밋
git checkout red     # test_t2_*.py + pytest.fail
git checkout green   # validate_lines.py + assert + 커밋
```

---

### 브랜치별 자주 하는 실수

| 브랜치 | 실수 | 올바른 처리 |
|--------|------|-------------|
| `spec` | `src/`에 함수 구현 | 문서·계약만. 구현은 `green` |
| `red` | `src/` 수정 또는 assert 작성 | `pytest.fail` 1줄만 |
| `green` | RED 여러 개 한 번에 구현 | 1 RED = 1 커밋 |
| `green` | GREEN 중 리팩터링 | REFACTOR 단계로 분리 |
| `main` | RED/GREEN 직접 진행 | `green`에서 완료 후 merge |

---

## 작업 방식 요약

### C2C (추적성)

```
PRD → To-Do → Test Case → 구현
```

- 판단 항목만 변환한다.
- **1 To-Do : 1 Test Case**
- **RED 먼저** (구현 전에 실패 확인)

### Dual-Track (ECB)

| Track | 레이어 | 테스트 경로 |
|-------|--------|-------------|
| B — Logic | Entity (도메인) | `tests/entity/` |
| A — UI | Boundary (입출력) | `tests/boundary/` |

Entity는 Boundary/Control를 **import하지 않는다** (순수 로직만).

### ARRR ↔ 명령 ↔ 모드

| 단계 | 명령 | 모드 |
|------|------|------|
| A — Ask (RED) | `/red-test-plan` → `/red-skeleton` 또는 `/tdd-red` | Ask / Agent |
| R — Respond (GREEN) | `/green-minimal` → `/golden-master` | Agent |
| R — Refine (REFACTOR) | `/refactor-smell` → `/refactor-safe` | Ask / Agent |
| R — Repeat | `/export` · `/export-session` | Agent |

---

## ① 주제 발견 — Mom Test (전 과정 Ask)

솔루션을 먼저 말하지 않고, **과거에 실제로 겪은 불편**을 한 문장으로 뽑는 단계입니다.  
이 단계는 ②~⑦ 전체에서 “왜 이 기능이 필요한가?”를 되묻는 **Ask**의 기준점이 됩니다.

### 3원칙

1. **내 아이디어 말하지 않기** — “자동 검증 앱” 같은 해답을 먼저 제시하지 않는다.
2. **과거·구체·사실만 묻기** — “지난주”, “20분”, “대각선”처럼 검증 가능한 사실만 받는다.
3. **칭찬·미래 의견 무시** — “좋을 것 같아요”, “있으면 편하겠죠”는 증거가 아니다.

### 좋은 답변 vs 나쁜 답변

| 구분 | 예시 | 이유 |
|------|------|------|
| ✅ 좋음 | “지난주 대각선 빼먹어 20분 날렸다” | 과거·구체·사실 |
| ❌ 나쁨 | “자동 검증 앱 있으면 좋겠다” | 솔루션(아이디어) |
| ✅ 좋음 | “행·열만 더하고 대각선은 나중에 확인해서 다시 계산했다” | 행동·시간 낭비가 드러남 |
| ❌ 나쁨 | “AI가 채워주면 학습에 도움될 것 같아요” | 미래 의견 |

### 산출물 — 진짜 문제 한 문장

Mom Test가 끝나면 아래 형식으로 **한 문장**만 남깁니다.

> **진짜 문제:** _(과거 사실 기반, 솔루션 없음)_

예시 (이 프로젝트에서 도출 가능한 문장):

> **진짜 문제:** 4×4 마방진을 손으로 채운 뒤 10개 줄(행·열·대각선) 합이 34인지 확인할 때, 빠진 줄이나 잘못된 줄을 찾는 데 시간이 많이 든다.

---

### Mom Test 프롬프트 입력 예

채팅(Agent/Ask)에 **아래 블록을 그대로** 붙여 넣어 Mom Test를 진행합니다.  
규칙: **질문 1개**, **솔루션 금지**, 답변 후 **사실성 평가 + 추궁 1개 + 불편 요약**.

#### 기본 템플릿

```
MagicSquare Mom Test. 페르소나: 부분 마방진(빈칸 2개) 학습자.
Mom Test 규칙 준수. 질문 1개만. 솔루션 금지.
→ 답변 후: 사실성 평가 + 다음 추궁 1개 + 불편 요약
```

#### 1회차 — 첫 질문 (시간·맥락)

```
MagicSquare Mom Test. 페르소나: 부분 마방진(빈칸 2개) 학습자.
Mom Test 규칙 준수. 질문 1개만. 솔루션 금지.

질문: 지난번 4×4 마방진을 손으로 채울 때, 맞는지 확인하는 과정에서
가장 오래 걸렸거나 다시 시작하게 만든 일이 무엇이었나요? 구체적인 날짜나
상황 하나만 말해 주세요.

→ 답변 후: 사실성 평가 + 다음 추궁 1개 + 불편 요약
```

**답변 예시 (학습자 역할):**

> 지난주 수요일 숙제로 빈칸 2개만 남긴 격자를 채웠는데, 행 네 개 합만 맞는지 보고 넘어갔다가 대각선을 빼먹어서 20분 더 썼다.

**에이전트가 돌려줄 응답 형식 (참고):**

| 항목 | 내용 |
|------|------|
| 사실성 평가 | ✅ 과거(지난주 수요일), ✅ 구체(20분), ✅ 행동(대각선 빼먹음) — 솔루션 없음 |
| 다음 추궁 1개 | 그때 **어느 줄**이 틀렸는지 알기 전까지 무엇을 반복했나요? (계산만? 격자 다시 채우기?) |
| 불편 요약 | 10선 중 일부만 검증 → 나중에 다시 확인 → **시간 낭비** |

#### 2회차 — 추궁 (어떤 줄을 놓쳤는지)

```
MagicSquare Mom Test. 페르소나: 부분 마방진(빈칸 2개) 학습자.
Mom Test 규칙 준수. 질문 1개만. 솔루션 금지.

이전 답변: 행만 확인하고 대각선을 빼먹어 20분 추가 소요.

질문: 그 20분 동안, 틀린 줄을 찾기 위해 실제로 한 행동을 순서대로
3단계 이내로만 말해 주세요. (앱·자동화 언급 금지)

→ 답변 후: 사실성 평가 + 다음 추궁 1개 + 불편 요약
```

**답변 예시:**

> 1) 행 합만 다시 더해 봤고 2) 그래도 이상해서 열을 더했는데 3) 그제야 대각선을 확인했다.

**에이전트 응답 형식 (참고):**

| 항목 | 내용 |
|------|------|
| 사실성 평가 | ✅ 검증 순서가 드러남 — **10선 전체를 한 번에 보지 않음** |
| 다음 추궁 1개 | 대각선에서 틀렸다는 걸 알았을 때, **몇 번째 줄**이라고 바로 말할 수 있었나요? |
| 불편 요약 | 실패 줄 **위치·ID**를 모름 → 원인 추적이 느림 |

#### 3회차 — 추궁 (실패 줄 식별)

```
MagicSquare Mom Test. 페르소나: 부분 마방진(빈칸 2개) 학습자.
Mom Test 규칙 준수. 질문 1개만. 솔루션 금지.

이전 답변: 대각선 확인 후에야 틀림을 알았고, 어느 줄인지 바로 말하기 어려웠다.

질문: 틀린 줄을 찾은 뒤에도 "R2"처럼 줄 이름을 바로 말하기 어려웠다면,
그때 격자에서 실제로 어떻게 표시했나요? (색칠, 동그라미, 메모 등 사실만)

→ 답변 후: 사실성 평가 + 다음 추궁 1개 + 불편 요약
```

**답변 예시:**

> 연필로 해당 행 전체에 밑줄만 그었다. 열은 나중에 따로 표시했다.

**에이전트 응답 형식 (참고):**

| 항목 | 내용 |
|------|------|
| 사실성 평가 | ✅ 수동 표시 — **줄 ID 체계 없음** |
| 다음 추궁 1개 | 빈칸이 아직 2개 남아 있을 때도, 지금까지 채운 숫자만으로 검증을 시도한 적이 있나요? |
| 불편 요약 | 미완성 격자 + **어떤 줄이 실패인지 즉시 판정 불가** |

#### 4회차 — 마무리 (미완성 격자)

```
MagicSquare Mom Test. 페르소나: 부분 마방진(빈칸 2개) 학습자.
Mom Test 규칙 준수. 질문 1개만. 솔루션 금지.

질문: 빈칸 2개가 남은 상태에서, 이미 채운 칸만으로 "아직 완성 전"인지
"틀렸는지" 구분하려고 한 적이 있나요? 있었다면 그때 막혔던 점을 한 가지만.

→ 답변 후: 사실성 평가 + 다음 추궁 1개 + 불편 요약 + 진짜 문제 한 문장 초안
```

**답변 예시:**

> 빈칸 때문에 합이 34가 안 나와서, 틀린 건지 아직 안 채운 건지 구분이 안 됐다.

**에이전트 응답 형식 (참고):**

| 항목 | 내용 |
|------|------|
| 사실성 평가 | ✅ incomplete vs fail 구분 필요성 — **② 설계 계약과 연결** |
| 다음 추궁 1개 | (마지막 회차) 위 불편을 **솔루션 없이** 한 문장으로 요약해 주세요. |
| 불편 요약 | 10선 합 검증 + 실패 줄 표시 + 미완성 구분이 동시에 필요 |
| **진짜 문제 한 문장** | 부분 마방진을 채우는 동안 10개 줄의 합(34)을 즉시 판정하고, 틀린 줄을 바로 알 수 없어 확인에 시간이 낭비된다. |

---

### Mom Test → ② 설계 연결

Mom Test에서 나온 불편이 아래 **설계 계약**으로 변환됩니다.

| Mom Test에서 드러난 사실 | 설계 반영 |
|-------------------------|-----------|
| 대각선을 빼먹음 | 10선: R1~R4, C1~C4, **D1, D2** |
| 틀린 줄을 바로 못 말함 | `fail` 시 **`failed_lines`** 반환 |
| 빈칸 때문에 합이 안 맞음 | `incomplete` vs `fail` **구분** |

---

## ② 설계 — R-G-I-O + `validate_lines` 계약

**브랜치:** `git checkout spec` — 상세 절차는 [브랜치별 작업 과정 → `spec`](#spec--설계-②) 참고.

### R-G-I-O (validate_lines)

| | 내용 |
|---|------|
| **R** Role | TDD·ECB를 지키는 시니어 개발자. Entity에 순수 도메인 로직만 두고, 10선 합 판정 계약을 테스트 가능하게 정의한다. |
| **G** Goal | 10선 합 34 **즉시 판정** + 틀렸을 때 **`failed_lines`** 로 실패 줄 표시. Mom Test 진짜 문제를 한 함수 계약으로 흡수한다. |
| **I** Input | 4×4 격자 (0=빈칸 `BLANK_CELL`, 1~16) |
| **O** Output | `status` (`pass` / `fail` / `incomplete`) + `fail`일 때만 `failed_lines` (R1~R4, C1~C4, D1, D2) |

### `incomplete` vs `fail` — Mom Test 연결

**연결 사실 (4회차):** "빈칸 때문에 합이 34가 안 나와서, 틀린 건지 아직 안 채운 건지 구분이 안 됐다."

| status | 학습자에게 의미 |
|--------|----------------|
| `incomplete` | 아직 완성 전 — 오류 아님 |
| `fail` | 다 채웠는데 틀림 — `failed_lines`로 어느 줄인지 표시 |

### validate_lines 계약

| status | 조건 |
|--------|------|
| `incomplete` | 격자에 `0`(빈칸)이 하나라도 있음 |
| `pass` | 16칸 모두 채워짐 + 10선 합이 모두 34 |
| `fail` | 어느 한 줄이라도 합 ≠ 34 → `failed_lines` 목록 반환 |

**줄 ID:** `R1`~`R4` (행), `C1`~`C4` (열), `D1`·`D2` (대각선)

### 프롬프트 입력 예 (설계 확인)

```
spec 브랜치. validate_lines 계약 검토.
입력: 4×4 격자 (0=빈칸). 출력: pass/fail/incomplete + failed_lines.
Mom Test 진짜 문제: "10선 합 즉시 판정 + 실패 줄 표시".
R-G-I-O 표를 채우고, incomplete와 fail이 구분되는 이유를
Mom Test 사실 1개와 연결해 설명해 주세요. 코드 작성 금지.
```

---

## ③ Ask (RED) — 의도적 실패

**브랜치:** `git checkout red`

### 목표

테스트만 작성하고 **`src/`는 수정하지 않는다.**  
`pytest` 결과가 **FAILED**이면 RED 성공이다. PASS면 구현이 이미 있는 것이므로 `src/`를 비우고 다시 시작한다.

### C2C 예시 (Dual-Track)

| | Track B (Logic) | Track A (Boundary) |
|---|-----------------|---------------------|
| PRD | 빈칸에 유효 숫자 입력 | grid=None 처리 |
| To-Do | 빈칸(0) 두 곳 찾기 | None → E003 |
| TC ID | `D-LOC-01` `find_blank_coords()` | `U-IN-01` |
| 테스트 경로 | `tests/entity/` | `tests/boundary/` |

### 프롬프트 입력 예 (RED)

```
/red-test-plan
Phase: red | Layer: entity | Target: D-LOC-01 (FR-LOC-01)
설계표만 작성. tests/ src/ 파일 생성 금지.
```

```
/red-skeleton
Test ID: D-LOC-01
Fixture: grid_g1 (tests/conftest.py)
src/ 수정 금지. pytest.fail 1줄만.
```

또는:

```
/tdd-red
D-LOC-01: find_blank_coords(grid_g1) → [(2,3),(4,4)] (1-index, row-major)
```

### validate_lines RED 예 (T2)

```
/red-skeleton
Test ID: T2 — test_t2_row_sum_not_34_is_fail
Given: 완성 마방진에서 (2,2) 값 6→7 변경
Then: status="fail", failed_lines에 "R2", "C2" 포함
Fixture: 완성 격자 fixture 필요 (conftest에 추가 요청)
src/ 수정 금지.
```

### 확인

```powershell
pytest tests/ -v
# → 1 failed = RED 정상
```

---

## ④ Respond (GREEN) — 최소 구현

**브랜치:** `git checkout green`

### GREEN 4단계

1. RED 재확인 (의도적 실패)
2. 통과할 **최소 코드만** `src/`에 작성 (`constants` SSOT)
3. `pytest.fail` → `assert` 교체 → **PASS**
4. `git commit` (**1커밋 = 1 RED**)

### 프롬프트 입력 예 (GREEN)

```
/green-minimal
RED 대상: D-LOC-01
src/entity/find_blank_coords.py 최소 구현.
MAGIC_CONSTANT·BLANK_CELL은 constants.py SSOT만 사용.
리팩터링 금지. 통과 후 커밋 메시지 초안 제안.
```

### Golden Master (회귀 안전망)

GREEN PASS 이후:

```
/golden-master
대상: D-LOC-01
순서: tests/_approval.py 연결 → UPDATE_GOLDEN=1 pytest → 검증 pytest
```

```powershell
$env:UPDATE_GOLDEN=1; pytest tests/entity/test_d_loc_01.py -v
pytest tests/entity/test_d_loc_01.py -v
```

---

## ⑤ Refine (REFACTOR) — 안전 정제

### 전제

`pytest` 전체 **PASS** + Golden Master 일치

### 프롬프트 입력 예

```
/refactor-smell
pytest 전체 PASS 확인됨. 수정 금지.
P0/P1 스멜 1~3개만 식별. (예: 10선 합산 중복)
```

```
/refactor-safe
P0: 10선 합산 중복 → _collect_failed_line_ids() 추출
계약 불변. ≤3 files, ≤3 methods.
pytest + golden matched 확인.
```

---

## ⑥ Repeat — 문서화 후 다음 RED

### 프롬프트 입력 예

```
/export
이번 ARRR 사이클: D-LOC-01
채팅에 있는 pytest 결과만 기재. 다음 RED 후보 1개 제안.
```

```
/export-session
세션에서 완료한 ARRR 사이클 목록 (최소 3회 권장).
```

**규칙:** 채팅에 없는 결과는 문서에 **기재하지 않는다.**

---

## ⑦ 확장 — 새 기능 = 새 ARRR 사이클

기능이 늘어날 때마다 ① Mom Test(필요 시) → ② 설계 → ③~⑥ ARRR를 **처음부터** 반복합니다.

### 확장 예시

| 새 기능 | Mom Test 질문 예 | 새 TC |
|---------|------------------|-------|
| 유효 숫자만 입력 | “1~16 밖 숫자 넣었을 때 어떻게 처리했나?” | `U-IN-02` |
| 힌트 1칸 | “막혔을 때 어떤 칸부터 다시 봤나?” | `D-HINT-01` |

### 프롬프트 입력 예 (확장 kickoff)

```
MagicSquare Mom Test. 페르소나: 부분 마방진(빈칸 2개) 학습자.
Mom Test 규칙 준수. 질문 1개만. 솔루션 금지.

새 기능 후보: "1~16 범위 밖 숫자 입력 방지"
질문: 지난번 격자에 0이나 17 같은 값을 넣었을 때, 그걸 언제 어떻게 알았나요?

→ 답변 후: 사실성 평가 + 다음 추궁 1개 + 불편 요약 + PRD 한 줄
```

---

## 실습 체크리스트

### 환경 (staging — 완료됨)

- [x] `pyproject.toml` + `src/` + `tests/`
- [x] `.cursorrules`
- [x] `/tdd-red` 등 슬래시 명령
- [x] 브랜치: `staging`, `spec`, `red`, `green`

### ① Mom Test

- [x] 프롬프트 1회차~4회차 진행
- [x] **진짜 문제 한 문장** 확정  
  > 부분 마방진을 채우는 동안 10개 줄의 합(34)을 즉시 판정하고, 틀린 줄을 바로 알 수 없어 확인에 시간이 낭비된다.

### ② spec

- [x] R-G-I-O 표 작성 (채팅 검토 완료 — 문서 반영됨)
- [ ] `validate_lines` 계약 **커밋** (`git checkout spec` 후 문서 커밋)

### ③ red

- [ ] `/red-skeleton` — 첫 TC (예: D-LOC-01 또는 T2)
- [ ] `pytest` → FAILED 확인

### ④ green

- [ ] `/green-minimal` — 최소 구현
- [ ] `/golden-master` — 회귀 안전망
- [ ] 1커밋 = 1 RED

### ⑤⑥ refactor + repeat

- [ ] `/refactor-smell` → `/refactor-safe`
- [ ] `/export` — ARRR 1사이클 보고
- [ ] **최소 3회** ARRR 반복

---

## 관련 문서

- [GitHub Push 가이드](./github-push-guide.md)
- 프로젝트 규칙: [`.cursorrules`](../.cursorrules)
- 실행: [AGENTS.md](../AGENTS.md)
