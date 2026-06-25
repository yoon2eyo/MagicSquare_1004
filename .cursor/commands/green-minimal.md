---
description: GREEN 최소 구현 — RED 1개당 1커밋
---

# /green-minimal

Phase: **green** | Layer: entity | Track: Logic

## RED 대상
채팅 또는 브랜치에서 현재 RED Test ID를 확인한다.

## GREEN 4단계
1. RED 재확인 (의도적 실패)
2. 통과할 **최소 코드만** `src/`에 작성 — `constants` SSOT 사용
3. 테스트에서 `pytest.fail` → `assert` 교체 → **PASS**
4. `git commit` (1커밋 = 1 RED)

## 금지
- 매직 넘버 하드코딩
- 여러 ID 동시 해결
- 리팩터링 (REFACTOR 단계에서)
- assert 완화

## 확인
```powershell
pytest tests/ -v
```
