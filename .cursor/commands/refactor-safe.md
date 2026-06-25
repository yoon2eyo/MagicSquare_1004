---
description: REFACTOR 안전 정제 — 계약 불변
---

# /refactor-safe

Phase: **refactor** | `/refactor-smell` 결과 기반

## 제약
- **계약 불변** (입력·출력·예외 변경 금지)
- 변경 예산: ≤3 files, ≤1 class, ≤3 methods
- 새 기능·버그 수정은 리팩터링이 아님

## 검증
```powershell
pytest tests/ -v
```
+ Golden Master matched

## 완료 후
`git commit` — 리팩터링만 포함
