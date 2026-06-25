# Project 개요

4×4 마방진 자동 검증 — TDD·ECB·ARRR 코딩 학습

## 구조

```
src/entity/     # 도메인 로직 (Boundary/Control import 금지)
src/control/    # 흐름 조합
src/boundary/   # UI·입출력
tests/entity/   # Track B — Logic
tests/boundary/ # Track A — UI
```

## 실행

```powershell
pip install -e ".[dev]"
pytest tests/ -v
```

## ARRR 명령

채팅에서 `/` 입력 → `tdd-red`, `red-skeleton`, `green-minimal` 등