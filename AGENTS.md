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

# Flask 데모 (구현 확인)
pip install -e ".[web]"
python -m src.boundary.flask_app
# → http://127.0.0.1:5000
```

## ARRR 명령

채팅에서 `/` 입력 → `tdd-red`, `red-skeleton`, `green-minimal` 등

## 요구 구체화 — Mom Test

**사용 시점:** 요구가 모호하거나 PRD/spec/TC에 연결되지 않은 **새 기능·Epic** 논의 시만.  
**사용 금지:** TC·spec·PRD 확정 후, RED/GREEN 구현, 버그 수정, 기술 세부.

1. 솔루션·기능 제안 금지  
2. 과거·구체·사실만 질문  
3. 미래 의견·칭찬은 근거로 쓰지 않음  

한 턴에 질문 1개 → 사실성 평가 → 추궁 1개 → 불편 요약 → **진짜 문제 한 문장**.  
확정 전 `src/`·`tests/` 작성 금지.

상세: [`docs/mom-test-guide.md`](docs/mom-test-guide.md)