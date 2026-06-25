---
description: RED 절차 버튼 — 의도적 실패 확인
---

# /tdd-red — RED 절차

현재 단계: **Ask (RED)**

## 수행 순서
1. 대상 Test ID 확인 (예: `D-LOC-01`, `T2`)
2. `tests/entity/` 또는 `tests/boundary/`에 테스트 스켈레톤 작성
3. Given-When-Then 주석 + `pytest.fail("RED: <ID> - No implementation, intentional failure")` **1줄만**
4. `pytest` 실행 → **FAIL이 정상** (PASS면 `src/`에 구현이 이미 있음 → 비우고 재시작)

## 제약
- **`src/` 수정 금지**
- `skip` / `xfail` 금지
- 설계표·계약과 1:1 추적 (C2C)

## 확인 명령
```powershell
pytest tests/ -v
```

FAIL 확인 후 사용자에게 GREEN 단계(`/green-minimal`) 진행 여부를 알린다.
